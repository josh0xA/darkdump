# Changelog

## [3.1.0] – 2025-07-17

### Added
* **User-Agent API demo** – `test_headers.py` showcasing every helper on the new `Headers` class.
* **Browser selection CLI switch** – `-b / --browser` option in `darkdump.py` to pick a UA family (Chrome, Firefox, IE / Edge, Opera, Safari, Mobile).

### Changed
#### `headers/agents.py`
* Refactored into a fully-featured **`Headers`** manager:
  * Categorised >200 UA strings by browser family.
  * Fixed one malformed UA and removed duplicates.
  * New helpers:
    * `get_random_agent()` – any UA.
    * `get_random_by_browser(browser_type)` – browser-specific UA.
    * `get_random_by_os(os_type)` – OS-specific UA.
    * `get_modern_agent()` – modern (2022+) UA.
  * Added doc-strings, type hints and runtime validation.
  * Maintains legacy `user_agents` list for backward compatibility.

#### `darkdump.py`
* Integrates the new `Headers` API:
  * Picks UA through the helper methods.
  * Accepts `-b / --browser` argument.
  * Debug mode now prints the selected UA.
* Minor docs & argument-parsing improvements.

### Documentation
* **README.md** updated:
  * Describes the new UA system and CLI switch.
  * Adds example commands and usage notes.

### Notes
* Version bumped to **3.1.0** to reflect backward-compatible feature upgrade.
