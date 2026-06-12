# Third-party notices

This project is derived from [hass-vw-eu-data-act](https://github.com/mikrohard/hass-vw-eu-data-act)
by Jernej Fijačko (MIT License). Cupra-specific OIDC configuration and branding
adaptations are maintained in this repository.

Additional API behaviour was documented from these MIT-licensed projects:

- [evcc](https://github.com/evcc-io/evcc) — `vehicle/vw/eudataact/`
- [ioBroker.vw-connect](https://github.com/TA2k/ioBroker.vw-connect) — `lib/euDataAct.js`

The EU Data Act data field dictionary is based on Volkswagen Group's published
**Continuous Data** dictionary PDF (`DataDictionary_V5.0_Continuous Data.pdf`,
document version **1.0.5**, 2026-02-25). The integration ships the parsed JSON
as `data_dictionary.json` (see `data_dictionary_meta.json` for provenance).
Regenerate with `tools/parse_dictionary.py` when the portal publishes an update.

## MIT License (hass-vw-eu-data-act)

Copyright (c) 2026 Jernej Fijačko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
