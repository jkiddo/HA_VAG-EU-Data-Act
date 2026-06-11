"""Offline tests for the HA-independent core (data.py + api.py helpers).

Loads the integration's pure modules without importing Home Assistant by
constructing a minimal `cupra_eu_data_act` package namespace and loading the
submodules that have no HA dependency.
"""
from __future__ import annotations

import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))

from _loader import FIXTURES, load_modules  # noqa: E402


def main() -> int:
    mods = load_modules("const", "data", "api")
    const = mods["const"]
    data = mods["data"]
    api = mods["api"]
    failures: list[str] = []

    def check(label, got, want):
        ok = got == want
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {got!r}" + ("" if ok else f" (want {want!r})"))
        if not ok:
            failures.append(label)

    # --- value parsing ----------------------------------------------------
    print("value parsing:")
    check("int", data.parse_value("116803", "int"), 116803)
    check("float", data.parse_value("0.0", "float"), 0.0)
    check("bool true", data.parse_value("true", "boolean"), True)
    check("bool false", data.parse_value("false"), False)
    check("duration 0s", data.parse_value("0s"), 0.0)
    check("duration 1800s", data.parse_value("1800s"), 1800.0)
    check("enum stays str", data.parse_value("WINDOW_HEATING_STATE_OFF"), "WINDOW_HEATING_STATE_OFF")
    check("empty -> None", data.parse_value(""), None)

    # --- dictionary -------------------------------------------------------
    print("data dictionary:")
    dd = data.load_dictionary()
    check("dict non-empty", len(dd) > 1000, True)
    check(
        "remaining_climate_time name",
        dd.get("3c19831c-38b8-3dc5-9ead-bb333616d925", {}).get("name"),
        "remaining_climate_time",
    )

    # --- dataset (committed fixture) --------------------------------------
    print("sample dataset:")
    sample_path = FIXTURES / "sample_dataset.json"
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    ds = data.Dataset.from_json(sample)
    check("vin", ds.vin, "WVWZZZTESTVIN0001")
    check("soc", _field_val(ds, "battery_state_report.soc"), 69)
    check("mileage", _field_val(ds, "mileage.value"), 116803)
    check("target_soc", _field_val(ds, "settings.target_soc"), 80)
    check("charge_power", _field_val(ds, "battery_state_report.charge_power"), 0.0)
    check("min_temperature", _field_val(ds, "min_temperature"), 19.5)
    check("locked", _field_val(ds, "locked"), True)
    check("parking_brake", _field_val(ds, "parking_brake"), True)
    check("remaining_climate_time", _field_val(ds, "remaining_climate_time"), 0.0)
    check("range", _field_val(ds, "range.value"), 312)
    check("captured_at present", ds.captured_at is not None, True)

    # --- duplicate field: deterministic selection regardless of order -----
    print("duplicate field selection:")
    dup_entries = [
        {"key": "ccc", "dataFieldName": "charging_state_report.current_charge_state", "value": "C"},
        {"key": "aaa", "dataFieldName": "charging_state_report.current_charge_state", "value": "A"},
        {"key": "bbb", "dataFieldName": "charging_state_report.current_charge_state", "value": "B"},
    ]
    picks = set()
    for order in ([0, 1, 2], [2, 1, 0], [1, 2, 0]):
        ds_d = data.Dataset.from_json(
            {"vin": "V", "user_id": "u", "Data": [dup_entries[i] for i in order]}
        )
        picks.add(_field_val(ds_d, "charging_state_report.current_charge_state"))
    check("stable pick under shuffle", picks, {"A"})

    # --- curated / raw classification ------------------------------------
    print("curated registry:")
    check("soc is curated", "battery_state_report.soc" in data.CURATED_FIELDS, True)
    check("locked is curated", "locked" in data.CURATED_FIELDS, True)
    check(
        "flat state_of_charge curated (PHEV)",
        "state_of_charge" in data.CURATED_FIELDS,
        True,
    )
    check(
        "flat remaining_charging_time curated",
        "remaining_charging_time" in data.CURATED_FIELDS,
        True,
    )
    check(
        "flat electr consumption curated",
        "long_term_data_average_electr_engine_consumption" in data.CURATED_FIELDS,
        True,
    )
    _mintemp = next(s for s in data.CURATED_SENSORS_DOTTED if s.field_name == "min_temperature")
    check("min_temperature named battery", _mintemp.name, "Battery min temperature")
    format_type = data.detect_dataset_format(ds.points)
    check("fixture format dotted", format_type, "dotted")
    curated_present = {dp.field_name for dp in ds.points.values()} & data.CURATED_FIELDS
    check("fixture has curated fields", len(curated_present) >= 5, True)

    # --- consumption transforms ------------------------------------------
    print("consumption transforms:")
    check(
        "fuel L/1000km -> L/100km",
        data.fuel_consumption_l_per_1000km_to_l_per_100km(168),
        16.8,
    )
    check(
        "electr kWh/1000km -> kWh/100km",
        data.electr_consumption_kwh_per_1000km_to_kwh_per_100km(180),
        18.0,
    )

    # --- raw unique_id namespaced by VIN (multi-vehicle) ----------------
    print("raw unique_id namespacing:")
    key = "1763a4fe-d8a6-3b8c-b095-70081f3e61c7"
    check("vin-prefixed", const.raw_unique_id("VINA", key), f"VINA_{key}")
    check("distinct per vehicle", const.raw_unique_id("VINA", key) != const.raw_unique_id("VINB", key), True)

    # --- sticky values ----------------------------------------------------
    print("sticky values:")
    check("fresh value kept", data.sticky(50, 55), 55)
    check("missing -> previous retained", data.sticky(55, None), 55)
    check("zero is not missing", data.sticky(55, 0), 0)
    check("false is not missing", data.sticky(True, False), False)

    # --- sentinel detection -----------------------------------------------
    print("sentinel detection:")
    check("uint32 max mileage", data.is_sentinel(4294967295, "mileage"), True)
    check("uint32 max mileage.value", data.is_sentinel(4294967295, "mileage.value"), True)
    check("uint16 max charging time", data.is_sentinel(65535, "remaining_charging_time"), True)
    check(
        "uint16 max dotted charging time",
        data.is_sentinel(65535, "battery_state_report.remaining_charging_time_complete"),
        True,
    )
    check(
        "-1 charging time (field-specific)",
        data.is_sentinel(-1, "remaining_charging_time"),
        True,
    )
    check(
        "-1 mileage NOT sentinel (might be valid)",
        data.is_sentinel(-1, "mileage"),
        False,
    )
    check("normal mileage 116803", data.is_sentinel(116803, "mileage"), False)
    check("zero is not sentinel", data.is_sentinel(0, "remaining_charging_time"), False)
    check("None is not sentinel", data.is_sentinel(None, "mileage"), False)
    check("string is not sentinel", data.is_sentinel("FOO", "state"), False)
    check("boolean True not sentinel", data.is_sentinel(True, "locked"), False)
    check(
        "uint32 max without field name",
        data.is_sentinel(4294967295),
        True,
    )
    check(
        "int32 max without field name",
        data.is_sentinel(2147483647),
        True,
    )

    # --- binary decoding --------------------------------------------------
    print("binary decoding:")
    check("open 2 -> True (door open)", data.decode_binary_state(2, "open"), True)
    check("open 3 -> False (door closed)", data.decode_binary_state(3, "open"), False)
    check("open 0 -> None (unsupported)", data.decode_binary_state(0, "open"), None)
    check("open 1 -> None (invalid)", data.decode_binary_state(1, "open"), None)
    check(
        "open invert 2 -> False (locked sensor on)",
        data.decode_binary_state(2, "open", invert=True),
        False,
    )
    check(
        "open invert 3 -> True (locked sensor off)",
        data.decode_binary_state(3, "open", invert=True),
        True,
    )
    check("onoff 0 -> False", data.decode_binary_state(0, "onoff"), False)
    check("onoff 1 -> True", data.decode_binary_state(1, "onoff"), True)
    check(
        "lights 0/1 -> None",
        (data.decode_binary_state(0, "lights"), data.decode_binary_state(1, "lights")),
        (None, None),
    )
    check("lights 2 -> False (off)", data.decode_binary_state(2, "lights"), False)
    check("lights 3 -> True (left)", data.decode_binary_state(3, "lights"), True)
    check("lights 4 -> True (right)", data.decode_binary_state(4, "lights"), True)
    check("lights 5 -> True (both)", data.decode_binary_state(5, "lights"), True)
    check("bool True passthrough", data.decode_binary_state(True), True)
    check(
        "bool False passthrough w/ invert",
        data.decode_binary_state(False, invert=True),
        True,
    )
    check("string -> None", data.decode_binary_state("OFF"), None)
    check("None -> None", data.decode_binary_state(None), None)

    # --- ApiError carries HTTP status ------------------------------------
    print("api error status:")
    err500 = api.ApiError("GET x -> HTTP 500", status=500)
    err_no = api.ApiError("Connection broken")
    check("status preserved on ApiError", err500.status, 500)
    check("status defaults to None", err_no.status, None)
    auth_err = api.AuthError("Login rejected")
    check("AuthError is ApiError", isinstance(auth_err, api.ApiError), True)
    check("AuthError default status None", auth_err.status, None)

    # --- find_by_field stability against shuffle ------------------------
    print("find_by_field:")
    points = {
        "ccc": data.DataPoint("ccc", "charging_state_report.current_charge_state", "C"),
        "aaa": data.DataPoint("aaa", "charging_state_report.current_charge_state", "A"),
        "bbb": data.DataPoint("bbb", "charging_state_report.current_charge_state", "B"),
    }
    dp = data.find_by_field(points, "charging_state_report.current_charge_state")
    check("smallest key wins", dp.key, "aaa")
    check("missing field -> None", data.find_by_field(points, "nope"), None)
    check(
        "Dataset.by_field still works",
        data.Dataset(
            vin="V", user_id=None, points=points
        ).by_field("charging_state_report.current_charge_state").key,
        "aaa",
    )

    # --- api zip helper ---------------------------------------------------
    print("api helpers:")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("WVWZZZTESTVIN0001_x.json", json.dumps(sample))
    parsed = api.EudaApiClient._unzip_json(buf.getvalue(), "x.zip")
    check("unzip vin", parsed["vin"], "WVWZZZTESTVIN0001")
    vins = api._extract_vins({"vehicles": [{"vin": "WVWZZZTESTVIN0001", "vehicleNickname": "Born"}]})
    check("extract_vins", vins, [{"vin": "WVWZZZTESTVIN0001", "nickname": "Born"}])

    # --- login field extraction -------------------------------------------
    print("login field extraction:")
    auth_page = (
        "<html><script>window._IDK = { templateModel: "
        '{"relayState":"RS","hmac":"HM","postAction":"login/authenticate",'
        '"error":null,"emailPasswordForm":{"email":"a@b.c"}}, '
        "csrf_token: 'CSRF1' }</script></html>"
    )
    f2, _ = api._login_fields(auth_page)
    check("templateModel hmac", f2.get("hmac"), "HM")
    check("templateModel _csrf", f2.get("_csrf"), "CSRF1")
    check("templateModel relayState", f2.get("relayState"), "RS")
    err_page = auth_page.replace('"error":null', '"error":{"text":"Bad creds"}')
    check("login error text", api._login_error(err_page), "Bad creds")
    email_page = (
        '<form action="/x/login/identifier"><input name=_csrf value=HC>'
        "<input name=hmac value=HH><input name=relayState value=RS><input name=email></form>"
    )
    fe, ae = api._login_fields(email_page)
    check("html-input _csrf not overridden", fe.get("_csrf"), "HC")
    check("html-input action", ae, "/x/login/identifier")

    # --- distance unit resolved from companion *.unit field ----------------
    print("distance unit resolution:")
    check("MILES -> mi", data.resolve_distance_unit("MILES"), "mi")
    check("KM -> km", data.resolve_distance_unit("KM"), "km")
    check("lowercase miles -> mi", data.resolve_distance_unit("miles"), "mi")
    check("unknown -> None", data.resolve_distance_unit("LIGHTYEARS"), None)
    mileage = next(s for s in data.CURATED_SENSORS_DOTTED if s.field_name == "mileage.value")
    check("mileage declares unit_field", mileage.unit_field, "mileage.unit")
    ds_mi = data.Dataset.from_json({"vin": "V", "user_id": "u", "Data": [
        {"key": "m1", "dataFieldName": "mileage.value", "value": "43531"},
        {"key": "m2", "dataFieldName": "mileage.unit", "value": "MILES"},
    ]})
    unit_dp = ds_mi.by_field("mileage.unit")
    check("resolved unit from dataset", data.resolve_distance_unit(unit_dp.value), "mi")

    # --- friendly names for bare fields ------------------------------------
    print("friendly raw names:")
    check("bare value -> description", data.friendly_name("value", "Value of the primary range"), "Value of the primary range")
    check("dotted name kept", data.friendly_name("battery_state_report.soc", "State of charge"), "battery_state_report.soc")
    check("bare value no desc -> value", data.friendly_name("value", None), "value")

    # --- enum integer fallback ---------------------------------------------
    print("enum integer fallback:")
    enum_desc = (
        "IMMEDIATE_ACTION_STAT E_INVALID, IMMEDIATE_ACTION_STAT E_IMMEDIATE_ACTION_TI ME, "
        "IMMEDIATE_ACTION_STAT E_IMMEDIATE_CHARGING , IMMEDIATE_ACTION_STAT E_IMMEDIATE_ACTION_ST OPPED, "
        "IMMEDIATE_ACTION_STAT E_IMMEDIATE_ACTION_R ANGE, IMMEDIATE_ACTION_STAT E_IMMEDIATE_ACTION_S OC, "
        "IMMEDIATE_ACTION_STAT E_CHARGE_MODE_SELEC TION"
    )
    members = data.enum_members(enum_desc)
    check("parses 7 enum members", len(members), 7)
    dp_int = data.DataPoint("k", "charging_state_report.immediate_action_state", "6", "enum", None, enum_desc)
    check("int 6 -> label", dp_int.value, "IMMEDIATE_ACTION_STATE_CHARGE_MODE_SELECTION")
    dp_str = data.DataPoint("k", "f", "IMMEDIATE_ACTION_STATE_IMMEDIATE_CHARGING", "enum", None, enum_desc)
    check("string label unchanged", dp_str.value, "IMMEDIATE_ACTION_STATE_IMMEDIATE_CHARGING")
    dp_prose = data.DataPoint("k", "report_type", "3", "enum", None, "The enum value of report type")
    check("prose enum desc -> int kept", dp_prose.value, 3)

    print()
    if failures:
        print(f"FAILED: {len(failures)} -> {failures}")
        return 1
    print("ALL OFFLINE TESTS PASSED")
    return 0


def _field_val(ds, field_name):
    dp = ds.by_field(field_name)
    return dp.value if dp else None


if __name__ == "__main__":
    raise SystemExit(main())
