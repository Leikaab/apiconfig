# apiconfig.config.providers

Dette modulpakken samler ulike "configuration providers" som kan hente innstillinger fra forskjellige kilder. Provider-klassene brukes typisk sammen med `ConfigManager` for å laste og slå sammen konfigurasjon før en `ClientConfig` opprettes.

## Innhold

- `env.py` – `EnvProvider` som leser fra miljøvariabler med et valgfritt prefiks og foretar enkel typegjettning.
- `file.py` – `FileProvider` som laster konfigurasjon fra en JSON-fil og støtter nøkkel-oppslag med punktnotasjon.
- `memory.py` – `MemoryProvider` som holder konfigurasjon i minnet, nyttig i tester eller som default-verdier.
- `__init__.py` – eksporterer de tre provider-klassene for enkel import.

## Eksempel på bruk

```python
from apiconfig.config.manager import ConfigManager
from apiconfig.config.providers import EnvProvider, FileProvider, MemoryProvider

providers = [
    EnvProvider(prefix="MYAPP_"),
    FileProvider(file_path="settings.json"),
    MemoryProvider(config_data={"timeout": 5}),
]

manager = ConfigManager(providers)
config_dict = manager.load_config()
```

Dette vil lese konfigurasjon fra miljøet, så fra `settings.json`, og til slutt overstyre med verdier fra `MemoryProvider`.

## Nøkkelklasser

| Klasse | Beskrivelse |
| ------ | ----------- |
| `EnvProvider` | Leser miljøvariabler med gitt prefiks og gjør enkel typekonvertering. |
| `FileProvider` | Laster konfigurasjon fra JSON-filer og gir tilgang via `get()` med punktnotasjon og typekoersjon. |
| `MemoryProvider` | Enkleste provider som returnerer et forhåndsdefinert dictionary. |
| `ConfigManager` | (Fra `config.manager`) Håndterer rekkefølge og sammenslåing av flere providers. |

## Design

Provider-klassene implementerer en enkel felleskontrakt: de tilbyr enten `load()` eller `get_config()` som returnerer et dictionary. `ConfigManager` bruker dette til å iterere gjennom en liste av providers og slå sammen resultatene. Mønsteret ligner på en strategisamling der hver provider er utskiftbar.

```mermaid
flowchart TD
    A[EnvProvider] -->|load()| M(Merged config)
    B[FileProvider] -->|load()| M
    C[MemoryProvider] -->|get_config()| M
    M --> D[ConfigManager]
```

## Testinstruksjoner

Kjør testene for provider-modulen slik:

```bash
pytest tests/unit/config/providers -q
```

## Status

Stabil – modulene er i aktiv bruk og dekkes av enhetstester.
