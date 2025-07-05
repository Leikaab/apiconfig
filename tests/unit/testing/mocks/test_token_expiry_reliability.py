# -*- coding: utf-8 -*-
"""Test to ensure token expiry mechanism is reliable under high load conditions."""

import threading
import time as time_mod
from concurrent.futures import Future, ThreadPoolExecutor, as_completed

import pytest

from apiconfig.testing.unit.mocks.auth import (
    AuthTestScenarioBuilder,
    MockBearerAuthWithRefresh,
)


class TestTokenExpiryReliability:
    """Test cases to ensure token expiry is reliable under various conditions."""

    def test_expiry_under_high_cpu_load(self) -> None:
        """Test token expiry works correctly even under high CPU load."""
        # Create a token that expires in 0.05 seconds
        strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(initial_token="load_test_token", expires_after_seconds=0.05)

        # Verify initial state
        assert not strategy.is_expired()

        # Create CPU load by spinning threads
        stop_flag = threading.Event()

        def cpu_burner() -> None:
            """Burn CPU cycles until stopped."""
            while not stop_flag.is_set():
                # Busy loop to consume CPU
                sum(range(1000))

        # Start multiple CPU-burning threads to simulate high load
        burn_threads: list[threading.Thread] = []
        for _ in range(10):  # 10 threads to really stress the system
            thread = threading.Thread(target=cpu_burner, daemon=True)
            thread.start()
            burn_threads.append(thread)

        try:
            # Wait for expiry time plus a small buffer
            time_mod.sleep(0.08)  # 0.05s expiry + 0.03s buffer

            # Check if token is expired - this should ALWAYS be True
            # With the old thread-based implementation, this could fail
            # under high load because the background thread might not run
            assert strategy.is_expired(), "Token should be expired after waiting past expiry time"
        finally:
            # Stop the CPU burner threads
            stop_flag.set()
            for thread in burn_threads:
                thread.join(timeout=0.1)

    def test_concurrent_expiry_checks(self) -> None:
        """Test multiple threads checking expiry status concurrently."""
        # Record the creation time before creating the strategy
        creation_time = time_mod.time()

        # Create a token that expires in 0.1 seconds
        strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(initial_token="concurrent_test_token", expires_after_seconds=0.1)

        results: list[tuple[float, bool]] = []

        def check_expiry() -> tuple[float, bool]:
            """Check expiry status and return timestamp and result."""
            timestamp = time_mod.time()
            is_expired = strategy.is_expired()
            return (timestamp, is_expired)

        # Use ThreadPoolExecutor to check expiry from multiple threads
        with ThreadPoolExecutor(max_workers=20) as executor:
            # Submit checks over a time period that spans the expiry
            futures: list[Future[tuple[float, bool]]] = []
            start_time = time_mod.time()

            # Submit checks for 0.2 seconds (before and after expiry)
            while time_mod.time() - start_time < 0.2:
                futures.append(executor.submit(check_expiry))
                time_mod.sleep(0.005)  # Small delay between submissions

            # Collect results
            for future in as_completed(futures):
                results.append(future.result())

        # Sort results by timestamp
        results.sort(key=lambda x: x[0])

        # Analyze results
        # All checks before expiry should return False
        # All checks after expiry should return True
        for timestamp, is_expired in results:
            time_since_creation = timestamp - creation_time
            if time_since_creation < 0.095:  # Small buffer for timing precision
                assert not is_expired, f"Token should not be expired at {time_since_creation:.3f}s"
            elif time_since_creation > 0.105:  # Small buffer for timing precision
                assert is_expired, f"Token should be expired at {time_since_creation:.3f}s"
            # Between 0.095 and 0.105, we don't assert anything due to timing precision

    def test_expiry_with_system_time_precision(self) -> None:
        """Test that expiry works correctly at the boundary of time precision."""
        # Test with very short expiry times
        for expiry_seconds in [0.001, 0.01, 0.05]:
            strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(
                initial_token=f"precision_test_{expiry_seconds}", expires_after_seconds=expiry_seconds
            )

            # Should not be expired immediately
            assert not strategy.is_expired()

            # Wait exactly the expiry time
            time_mod.sleep(expiry_seconds)

            # Should be expired now (or very close to it)
            # We allow one more check in case we're right at the boundary
            is_expired_1 = strategy.is_expired()
            time_mod.sleep(0.001)  # Tiny additional wait
            is_expired_2 = strategy.is_expired()

            assert is_expired_1 or is_expired_2, f"Token with {expiry_seconds}s expiry should be expired after waiting"

    def test_manual_expiry_overrides_timestamp(self) -> None:
        """Test that manual expiry setting works correctly with timestamp-based expiry."""
        # Create a token that expires in 1 second (far in the future for this test)
        strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(initial_token="manual_override_token", expires_after_seconds=1.0)

        # Should not be expired initially
        assert not strategy.is_expired()

        # Manually expire it
        strategy.set_expired(True)
        assert strategy.is_expired()

        # Un-expire it manually
        strategy.set_expired(False)
        assert not strategy.is_expired()

        # Wait past the original expiry time
        time_mod.sleep(1.1)

        # Should be expired now due to timestamp
        assert strategy.is_expired()

    @pytest.mark.parametrize("delay_ms", [1, 5, 10, 50, 100])
    def test_various_expiry_delays(self, delay_ms: int) -> None:
        """Test token expiry with various delay values."""
        delay_seconds = delay_ms / 1000.0

        strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(initial_token=f"delay_test_{delay_ms}ms", expires_after_seconds=delay_seconds)

        # Not expired initially
        assert not strategy.is_expired()

        # Wait for expiry
        time_mod.sleep(delay_seconds * 1.2)  # 20% buffer

        # Should be expired
        assert strategy.is_expired()


class TestRaceConditionPrevention:
    """Tests specifically designed to catch race conditions."""

    def test_no_background_threads_created(self) -> None:
        """Verify that token expiry doesn't create background threads."""
        initial_thread_count = threading.active_count()

        # Create multiple expiry scenarios
        strategies: list[MockBearerAuthWithRefresh] = []
        for i in range(10):
            strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(initial_token=f"thread_test_{i}", expires_after_seconds=0.1 * (i + 1))
            strategies.append(strategy)

        # Check thread count hasn't increased
        # (The old implementation would have created 10 new threads)
        new_thread_count = threading.active_count()
        assert new_thread_count == initial_thread_count, (
            f"No new threads should be created. Initial: {initial_thread_count}, " f"New: {new_thread_count}"
        )

    def test_deterministic_expiry_behavior(self) -> None:
        """Test that expiry behavior is deterministic and repeatable."""
        expiry_time = 0.05

        # Run the same test multiple times
        for run in range(5):
            strategy = AuthTestScenarioBuilder.create_token_expiry_scenario(
                initial_token=f"deterministic_test_run_{run}", expires_after_seconds=expiry_time
            )

            # Take measurements at specific intervals
            measurements: list[tuple[float, bool]] = []
            start_time = time_mod.time()

            # Measure every 10ms for 100ms
            for _ in range(10):
                is_expired = strategy.is_expired()
                elapsed = time_mod.time() - start_time
                measurements.append((elapsed, is_expired))
                time_mod.sleep(0.01)

            # Verify the transition happens at the expected time
            for elapsed, is_expired in measurements:
                if elapsed < expiry_time:
                    assert not is_expired, f"Run {run}: Should not be expired at {elapsed:.3f}s"
                elif elapsed > expiry_time + 0.01:  # Small buffer for timing
                    assert is_expired, f"Run {run}: Should be expired at {elapsed:.3f}s"
