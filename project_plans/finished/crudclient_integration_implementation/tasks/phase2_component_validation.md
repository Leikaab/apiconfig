# Phase 2 Component Validation

## Overview
Validate that all Phase 2 testing enhancement components work together and provide comprehensive testing utilities for auth scenarios that both `apiconfig` and `crudclient` can leverage. These tests use mocked dependencies and do not hit real external APIs.

## Objective
Ensure all Phase 2 testing utilities are properly integrated, functional, and provide the expected capabilities for auth verification and enhanced mocking scenarios using component-level testing with mocks.

## Requirements

### 1. Auth Verification Component Testing
Test all verification utilities with mocked auth scenarios:

```python
# tests/component/test_auth_verification_integration.py
def test_auth_verification_component_integration():
    """Test that auth verification utilities work with mocked auth strategies."""
    # Test Basic Auth verification with mocked strategy
    mock_basic_auth = Mock()
    mock_basic_auth.prepare_request_headers.return_value = {"Authorization": "Basic dXNlcjpwYXNz"}

    headers = mock_basic_auth.prepare_request_headers()
    assert AuthHeaderVerification.verify_basic_auth_header(headers["Authorization"])

    # Test Bearer Auth verification with mocked strategy
    mock_bearer_auth = Mock()
    mock_bearer_auth.prepare_request_headers.return_value = {"Authorization": "Bearer test_token"}

    headers = mock_bearer_auth.prepare_request_headers()
    assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

    # Test API Key verification with mocked strategy
    mock_api_key_auth = Mock()
    mock_api_key_auth.prepare_request_headers.return_value = {"X-API-Key": "test_key"}

    headers = mock_api_key_auth.prepare_request_headers()
    assert AuthHeaderVerification.verify_api_key_header(headers["X-API-Key"], "test_key")
```

### 2. Enhanced Mock Component Validation
Test enhanced mocks work with refresh flows using component-level testing:

```python
# tests/component/test_enhanced_auth_mocks_refresh.py
def test_enhanced_auth_mocks_refresh_component():
    """Test that enhanced auth mocks support refresh scenarios in component tests."""
    # Test mock auth strategy with refresh capabilities
    mock_auth = MockAuthStrategy()
    mock_auth.configure_refresh_behavior(can_refresh=True, refresh_success=True)

    assert mock_auth.can_refresh()
    result = mock_auth.refresh()
    assert result is not None
    assert "token_data" in result

    # Test refresh failure scenarios with mock injection
    mock_auth.configure_refresh_behavior(can_refresh=True, refresh_success=False)
    with pytest.raises(TokenRefreshError):
        mock_auth.refresh()

    # Test refresh callback integration
    callback = mock_auth.get_refresh_callback()
    assert callback is not None
    assert callable(callback)

    # Test callback execution (should not raise)
    callback()
```

### 3. Cross-Component Integration Testing
Test that all Phase 2 components work together in component-level scenarios:

```python
# tests/component/test_phase2_cross_component_integration.py
def test_phase2_cross_component_integration():
    """Test that verification and mocking work together in component tests."""
    # Create a mock auth strategy with realistic behavior
    mock_auth = MockAuthStrategy()
    mock_auth.configure_headers({"Authorization": "Bearer mock_token_12345"})
    mock_auth.configure_refresh_behavior(can_refresh=True, refresh_success=True)

    # Get headers from mock
    headers = mock_auth.prepare_request_headers()

    # Verify headers using verification utilities
    assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

    # Verify headers using verification utilities
    assert AuthHeaderVerification.verify_bearer_auth_header(headers["Authorization"])

    # Test refresh flow integration
    if mock_auth.can_refresh():
        old_token = token
        result = mock_auth.refresh()

        # Verify refresh result structure
        assert "token_data" in result
        assert "access_token" in result["token_data"]

        # Get new headers and verify they're different
        new_headers = mock_auth.prepare_request_headers()
        new_token = new_headers["Authorization"][7:]  # Remove "Bearer " prefix
        assert new_token != old_token
```

### 5. Error Scenario Component Testing
Test error handling across all Phase 2 components:

```python
# tests/component/test_phase2_error_scenarios.py
def test_phase2_error_scenarios_component():
    """Test error handling across Phase 2 components in component test scenarios."""
    # Test verification with invalid headers
    with pytest.raises(AuthHeaderVerificationError):
        AuthHeaderVerification.verify_bearer_auth_header("Invalid Bearer")

    # Test extraction with malformed headers
    with pytest.raises(AuthenticationError):
        # Test basic auth extraction with malformed header
        import base64
        try:
            encoded_credentials = "Malformed Basic"[6:]  # Remove "Basic "
            base64.b64decode(encoded_credentials).decode('utf-8')
        except Exception:
            raise AuthenticationError("Invalid Basic auth format")

    # Test mock error injection
    mock_auth = MockAuthStrategy()
    mock_auth.configure_error_injection(TokenRefreshError("Simulated refresh failure"))

    with pytest.raises(TokenRefreshError):
        mock_auth.refresh()
```

## Implementation Steps

1. **Create component test files** in `tests/component/` directory
2. **Import all Phase 2 components** (verification, extraction, enhanced mocks)
3. **Create comprehensive component test scenarios** covering all integration points with mocks
4. **Test error scenarios** and edge cases with mock injection
5. **Validate performance** of testing utilities in component scenarios
6. **Create documentation examples** based on working component tests

## Files to Create/Modify
- `tests/component/test_auth_verification_integration.py` (new)
- `tests/component/test_enhanced_auth_mocks_refresh.py` (new)
- `tests/component/test_phase2_cross_component_integration.py` (new)
- `tests/component/test_phase2_error_scenarios.py` (new)

## Dependencies
- [Phase 2, Task 1: Auth Verification Utilities](phase2_task1_auth_verification.md)
- [Phase 2, Task 2: Enhanced Auth Mocks](phase2_task2_enhanced_auth_mocks.md)

## Quality Gates

### Component Testing
- [ ] All verification utilities work with mocked auth strategies
- [ ] All extraction utilities work with mocked auth strategy outputs
- [ ] Enhanced mocks support refresh scenarios correctly in component tests
- [ ] Cross-component integration functions properly with mocked dependencies

### Performance
- [ ] Testing utilities perform efficiently in component test scenarios
- [ ] No significant overhead introduced by mocking layers
- [ ] Memory usage is reasonable for component test scenarios

### Documentation
- [ ] Component test examples are clear and comprehensive
- [ ] Error scenarios are documented with mock injection examples
- [ ] Usage patterns are demonstrated in component test context

## Success Criteria
- [ ] All Phase 2 testing utilities integrate seamlessly in component tests
- [ ] Comprehensive component test coverage for all integration scenarios
- [ ] Clear documentation and examples for users in component test context
- [ ] Performance meets expectations for testing utilities
- [ ] Error handling works correctly across all components with mock injection

## Test Categorization
- **Unit Tests**: Individual utility method testing (in individual task files)
- **Component Tests**: Multi-utility testing with mocks (this validation task)
- **Integration Tests**: Real external API testing (Phase 3 only, tech lead supervised)

## Notes
- Focus on component-level usage patterns that `crudclient` would use with mocked dependencies
- Ensure testing utilities are easy to use and understand in component test scenarios
- Validate that mocks provide realistic behavior for development/testing
- Consider edge cases and error scenarios with mock injection
- **No real external API calls** - all interactions are mocked

## Estimated Effort
3-4 hours

## Next Phase
[Phase 3: Foundation & Polish](../orchestrator_plan.md#phase-3-foundation--polish-low-priority)