"""Fail-closed validation for the evidence, 2D, 3D, and camera manifests."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Iterable
from datetime import date
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from . import course_runtime as course_runtime_pipeline
from . import generated_artifacts as generated_artifacts_pipeline
from . import layout as layout_pipeline
from . import quality as quality_pipeline
from . import scene as scene_pipeline
from . import shots as shots_pipeline
from . import tokens

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
EVIDENCE = ROOT / "evidence" / "abilene.yaml"
COURSE = ROOT / "course" / "segments.yaml"
COURSE_VISUALS = ROOT / "course" / "visuals.yaml"

MASTER_FIELDS = {
    "meta",
    "reference_campus",
    "status_styles",
    "copy",
    "nodes",
    "edges",
}
MASTER_META_FIELDS = {
    "version",
    "status",
    "reference_as_of",
    "evidence_file",
    "diagram_posture",
    "journey",
    "journey_bar",
    "gigawatts_to_tokens_funnel",
}
MASTER_REFERENCE_CAMPUS_FIELDS = {
    "name",
    "location",
    "atlas_stable_key",
    "atlas_source",
    "scope_boundary",
}
MASTER_JOURNEY_FIELDS = {"electrical", "thermal"}
MASTER_ELECTRICAL_JOURNEY_FIELDS = {
    "grid_138",
    "grid_345",
    "behind_the_meter",
}
MASTER_JOURNEY_BAR_FIELDS = {"electrical", "thermal"}
MASTER_STATUS_STYLE_FIELDS = {"line", "meaning"}
MASTER_STATUS_STYLE_IDS = {
    "energized",
    "permitted",
    "future_design",
    "conceptual",
    "course_variant",
}
MASTER_COPY_TEXT_FIELDS = {"text"}
MASTER_COPY_HIDDEN_TEXT_FIELDS = {"text", "base_visible"}
MASTER_COPY_TEMPLATE_FIELDS = {"template", "facts"}
MASTER_COPY_UNKNOWN_TEMPLATE_FIELDS = {"template", "facts", "posture"}

NODE_FIELDS = {
    "id",
    "label",
    "domain",
    "gate",
    "presence",
    "lifecycle",
    "as_of",
    "source_ids",
    "fact_ids",
}
NODE_OPTIONAL_FIELDS = {"base_visible", "reveal_copy_ids"}
EDGE_FIELDS = {
    "id",
    "from",
    "to",
    "carries",
    "presence",
    "lifecycle",
    "normal_state",
    "flow_direction",
    "source_ids",
    "fact_ids",
}
EDGE_OPTIONAL_FIELDS = {"base_visible", "reveal_copy_ids"}
NODE_PRESENCES = {
    "course_variant",
    "physical_sink",
    "platform_evidenced",
    "site_evidenced",
    "teaching_reference",
}
EDGE_PRESENCES = NODE_PRESENCES - {"physical_sink"}
EDGE_NORMAL_STATES = {"available_if_built", "not_physical", "unknown"}
EDGE_FLOW_DIRECTIONS = {"bidirectional", "forward", "none"}
EVIDENCED_PRESENCES = {"site_evidenced", "platform_evidenced"}
NODE_PRESENCE_LIFECYCLES = {
    "site_evidenced": {"conceptual", "energized", "future_design", "permitted"},
    "platform_evidenced": {"conceptual", "operational_confirmed"},
    "teaching_reference": {"conceptual"},
    "course_variant": {"course_variant"},
    "physical_sink": {"terminal"},
}
EDGE_PRESENCE_LIFECYCLES = {
    "site_evidenced": {"conceptual", "energized", "permitted"},
    "platform_evidenced": {"conceptual"},
    "teaching_reference": {"conceptual"},
    "course_variant": {"course_variant"},
}
TOPOLOGY_PRESENCE_CONTRACT = MappingProxyType(
    {
        "node:gas_turbine": "site_evidenced",
        "node:generator": "site_evidenced",
        "node:gsu_transformer": "teaching_reference",
        "node:utility_source_138": "site_evidenced",
        "node:initial_tie_138": "site_evidenced",
        "node:initial_substation_138": "site_evidenced",
        "node:utility_source_345": "site_evidenced",
        "node:transmission_corridor_345": "site_evidenced",
        "node:hv_protection_envelope_345": "site_evidenced",
        "node:campus_substation_lpt_345": "site_evidenced",
        "node:nuclear_ppa": "course_variant",
        "node:campus_mv_distribution": "teaching_reference",
        "node:bess_package": "site_evidenced",
        "node:diesel_backup_package": "site_evidenced",
        "node:unit_substation": "teaching_reference",
        "node:lv_switchgear": "teaching_reference",
        "node:ups": "teaching_reference",
        "node:busway": "teaching_reference",
        "node:power_shelf": "platform_evidenced",
        "node:vrm": "teaching_reference",
        "node:die": "platform_evidenced",
        "node:rack_air_load": "platform_evidenced",
        "node:cold_plate": "platform_evidenced",
        "node:rack_manifold": "platform_evidenced",
        "node:cdu": "teaching_reference",
        "node:crah": "teaching_reference",
        "node:facility_loop": "site_evidenced",
        "node:air_cooled_chiller": "site_evidenced",
        "node:fill_treatment": "site_evidenced",
        "node:atmosphere": "physical_sink",
        "edge:btm_fuel_to_shaft": "site_evidenced",
        "edge:btm_terminal_to_gsu": "teaching_reference",
        "edge:btm_gsu_to_mv": "teaching_reference",
        "edge:grid138_source_to_tie": "site_evidenced",
        "edge:grid138_tie_to_station": "site_evidenced",
        "edge:grid138_station_to_mv": "teaching_reference",
        "edge:grid345_source_to_corridor": "site_evidenced",
        "edge:grid345_corridor_to_hv": "site_evidenced",
        "edge:grid345_hv_to_lpt": "site_evidenced",
        "edge:grid345_lpt_to_mv": "teaching_reference",
        "edge:nuclear_ppa_overlay": "course_variant",
        "edge:bess_to_mv": "teaching_reference",
        "edge:diesel_to_mv": "teaching_reference",
        "edge:mv_to_unit_sub": "teaching_reference",
        "edge:unit_sub_to_lv": "teaching_reference",
        "edge:lv_to_ups": "teaching_reference",
        "edge:ups_to_busway": "teaching_reference",
        "edge:busway_to_power_shelf": "platform_evidenced",
        "edge:power_shelf_to_vrm": "platform_evidenced",
        "edge:vrm_to_die": "teaching_reference",
        "edge:die_to_cold_plate_heat": "platform_evidenced",
        "edge:cold_plate_to_manifold_return": "platform_evidenced",
        "edge:manifold_to_cdu_return": "teaching_reference",
        "edge:cdu_to_manifold_supply": "teaching_reference",
        "edge:manifold_to_cold_plate_supply": "platform_evidenced",
        "edge:cdu_to_facility_return": "teaching_reference",
        "edge:facility_to_cdu_supply": "teaching_reference",
        "edge:rack_air_load_to_crah": "teaching_reference",
        "edge:crah_to_facility_return": "teaching_reference",
        "edge:facility_to_crah_supply": "teaching_reference",
        "edge:facility_to_chiller_return": "site_evidenced",
        "edge:chiller_to_facility_supply": "site_evidenced",
        "edge:chiller_to_atmosphere": "site_evidenced",
        "edge:fill_to_facility_loop": "site_evidenced",
    }
)
EVIDENCE_FIELDS = {
    "schema_version",
    "subject",
    "accessed_as_of",
    "evidence_boundary",
    "sources",
    "facts",
}
FACT_FIELDS = {
    "value",
    "unit",
    "scope",
    "basis",
    "lifecycle",
    "as_of",
    "source_ids",
    "posture",
}
SOURCE_FIELDS = {
    "publisher",
    "title",
    "kind",
    "url",
    "publication_date",
    "review_date",
    "accessed_as_of",
    "date_note",
}
SOURCE_PAYLOAD_FIELDS = (
    "publisher",
    "title",
    "kind",
    "url",
    "publication_date",
    "review_date",
    "accessed_as_of",
    "date_note",
)
SOURCE_PAYLOAD_CONTRACT = MappingProxyType(
    {
        "abilene:crusoe_abilene_cooling_2025": "9c1a40ae82a1ec9185370b3b45dabcad9e8ff857062371fe29a8af92be6f1453",
        "abilene:crusoe_abilene_expansion_2025": "b356ed74a07ab26983fc72699fe6080695c9bc819af5d2bf9f63dde7f1da7980",
        "abilene:crusoe_abilene_live_2025": "85ec904548e3e5623d6a5a1376e7452f5236593beef592af4e332afa93189d6a",
        "abilene:crusoe_microsoft_expansion_2026": "702734dbb60bc5672f4c0f097cb84fd0ce3c0ab5364d332cea62821e3ca76543",
        "abilene:mortenson_abilene_power_delivery": "7a1b432a8d32c1db4f6a60ade2df1a0a6bfcea5eb227ae787388ea480033ca32",
        "abilene:nvidia_dgx_gb200_hardware": "95ad940e23858f6f7d281e8a4b0b14124cceff0bbe2faca616d8fa4c50c77dc6",
        "abilene:openai_stargate_oracle_2025": "629be667b37ae7c65770669cfa799deba6b373d043869c35b257c4dbf57fb049",
        "abilene:oracle_abilene_facts": "f7be4589c88bc8d0fd8508f58e02215c0427a5fbf89dff7bae0218bcaa3aa018",
        "abilene:oracle_abilene_portfolio": "4b3948b16b82bb37d46c146d3a267a560fb756a5af7e0952746999faef2564f8",
        "abilene:solar_titan_350_datasheet": "b63317dd99b0e6f855f1d9fe6e14a385904c7640ef23e1753c14f89a656343c7",
        "abilene:tceq_177262_diesel_application": "7f70f82ce2c4c0f8cb7643650a60560d39b172cfc04660df2e80450cc405f9c9",
        "abilene:tceq_177262_diesel_review": "244cef8f72f6738a19ce7a7876ba06aaf8aff9d5e65e043ed8c6dfc1a160e733",
        "abilene:tceq_177263_gas_review": "baabb154c139133ab391947bc4d097137c66e05097258277aa474b53f9a9ff6d",
        "abilene:tceq_37589_reference_drawing": "b88284ca61f8ddda5bd6daf05999d11eb8be40370179c8a07992ab58c977b503",
        "abilene_execution:aep_july_2025_construction_report": "6bf5787b6b7062c9d1d9afd7ed701e30017266263f2df80694a4907372e1f93e",
        "abilene_execution:aep_september_2023_construction_report": "3ba3e7e2f16af7ba4a05be325b0cb395a5952c43c4ad761f79a63548bf061041",
        "abilene_execution:crusoe_abilene_award_2025": "fcbea36a50cccce3ed3dd420adf98c6da6cf01c429fba59e13fac85b32658382",
        "abilene_execution:crusoe_abilene_live_2025": "2a4c57c34c705b6821b94ca5ccb9ee4d21a18be3fee583cf959ab23ec4fb091a",
        "abilene_execution:crusoe_energy_current": "3f24547e00fc2887a972ad8915b5627592d70f3ecff6ae7cb9813abea677aef6",
        "abilene_execution:crusoe_inside_abilene_2025": "bfd411e269aa4cc9320532b79dd2578dc937b5c52f8ef97aebd26805955ae4e3",
        "abilene_execution:crusoe_microsoft_expansion_2026": "93f297f1f3390d11333050689588fb291e979978ac60d23a180e6cadd57c82bd",
        "abilene_execution:ercot_nprr1267": "a9fa54f4d227038d2e67ed20b6211c454f5ed2a0b1d5c13dd6adb0090d51ca09",
        "abilene_execution:mortenson_abilene_power_delivery": "2b95712740c1fca0f68f9b7d4e111f99d9e7d373a179f86b1299ca3b82765466",
        "abilene_execution:nvidia_dgx_gb200_hardware": "e349112c4569e60dfeddc4f6f4f4516a8823512c0f867e79d039358ac11cac2b",
        "abilene_execution:tceq_177263_gas_review": "0a5739224ffae9a2a23e31feb38e4d9088181bff160daed3b7b4960a1ad0c80e",
        "abilene_execution:tceq_37589_reference_drawing": "80f484f79b26304381fcdf02a2a1a7b58cf2c36de2a2034010208d706eb4e973",
        "commercial_compute:coreweave_2025_10k": "389486fee4ce0b9f768e23ea14fa37f563d2fa6ab357468a31f98a1ec60d3eba",
        "commercial_compute:crusoe_abilene_phase1_jv_2024": "ba51d70c031ad79ce42b14c102b27debbb3cf5e444a0797b8cf233d9a44df780",
        "commercial_compute:crusoe_abilene_phase2_jv_2025": "114b124d975c9b9cba1e2cea73c329b4e7c2299d4f6015809dea248a298f0a33",
        "commercial_compute:crusoe_lancium_abilene_2024": "bfb9f5ee1e0797eb38ff8c12263c7d1791acf32c274bbfdaa75a1ce02ae8cf46",
        "commercial_compute:equinix_2025_10k": "219e5f7319bfe228c1e3fc27937e6041955a01cb6667a6d6983ca3e3162c802c",
        "commercial_compute:iso_iec_30134_2_2026": "2fcb8295239e58df0f1e2086a11d1d25ea5b1168c61299b568cd3c27b088eed2",
        "commercial_compute:microsoft_2025_annual_report": "7c485f9601bba1facf7539b30fda6fd37fc72c093ef55910735ac210013a84b2",
        "commercial_compute:mlcommons_inference_rules": "44c9358180865bdc3fbec72d891d467abc8276966e1dbf0c699db7c7dfff4acc",
        "commercial_compute:nvidia_dgx_gb_hardware_2026": "351420aafbeb35982879a4d4cc3127d422de5e70ab2c5f3cb3be8af9428f9b9a",
        "commercial_compute:nvidia_triton_batching_2_59_1": "d92f451b27eeb9fd5c6d6d4b20ad360c3c3797bff533804a1c38dac487b8ca9b",
        "commercial_compute:openai_stargate_formation_2025": "6da7c0b070e004fa210babbd178e2ee36b45103f568489702803e229efc313da",
        "commercial_compute:openai_stargate_oracle_2025": "231f3f94dc64a5f407edc88a9c4287632f6eb8f45f0809788807fcacfca9cfcc",
        "commercial_compute:oracle_abilene_2026": "4e2ef3e2c7c94f8fbc85c7ed04259c1827170d73cbe9fef5e1962078826eab3e",
        "commercial_compute:palm_2022": "dd307415656bfc9c74d44f479e61331ac7b4325af62bc6a4b2e12591d328e0a5",
        "commercial_energy:constellation_crane_microsoft_ppa": "27344ee2d98c2732bc03d7298ebc255c6397fd501018dc82dc5d7330cbea48fb",
        "commercial_energy:ghg_protocol_scope_2_guidance": "508901bb8e7a5a341994a547f2fe9dac1d8ec0ac073dc7b0424aa3c6acec6dfa",
        "delivery_resilience:doe_lpt_resilience_2024": "e176229ec870f34aed47a7f4f929767de505d8293df27e663a1d2dab211bf476",
        "delivery_resilience:doe_pnnl_data_center_emt_2025": "dfd93f6442bfa32088570879eafb8267533f02150f80c696be548fafcd3ab715",
        "delivery_resilience:doe_transformer_market_analysis": "96136895bcf025b7368222901bdf17b11b9c34e4e45696c4b54d65b63db0391b",
        "delivery_resilience:ge_vernova_investor_update_2024": "4488ddeafbd10b7ed045dff11874a00f8a44f4ab3ce235cf7397c8b220530deb",
        "delivery_resilience:ge_vernova_investor_update_2025": "a03d4a267fad7e85060e49a33d1b0c00494c7683adc201df7876e3d46d88fbbd",
        "delivery_resilience:google_ml_power_shaping_2025": "0d081e396292eae08670c7da54a90090bee1b37225bf008c9ebf92f2138358ca",
        "delivery_resilience:nerc_emerging_large_loads_2025": "3e53d073d3bdb92a14353caca9fd0cb7cda48efd7b55929d87499c42518fdc62",
        "delivery_resilience:nerc_voltage_sensitive_load_incident_2025": "22c36bc4b8fbefdbfd997af29c0a0285e9cd9718af61cad14acd308ffc820d19",
        "delivery_resilience:schneider_liquid_cooling_commissioning_2026": "eecc3fe1b051c4831e05852dfb83df0e6723670c06f9b2bc76fdc35f7c81354c",
        "delivery_resilience:schneider_uniflair_xca_2026": "73480947249917afc4026902cb89c0bb15c2199ae786f35b0ae6ffe717b87a7e",
        "delivery_resilience:tceq_37589_reference_drawing": "b294e63b91460d89f6d91d25c2f4c35e2da998bba057721b6ce690f1ee65fd14",
        "delivery_resilience:vertiv_coolphase_row": "c1ad4f7aba27839bb896ee06ec574a3d5e8227923bef3290c189199a02539535",
        "delivery_resilience:vertiv_ups_bess_roles_2026": "52e8b4e5920c5280052c3eaae17ed74b1eca454ec0f068c06e2c68298e1cdfb0",
        "electrical_engineering:eia_electricity_generation": "c948fd2ca47bc5ce90db48d7a08866e726d98c4803ec2980d28800b4cd69b2c8",
        "electrical_engineering:hitachi_generator_step_up_transformers": "74ecd6caaf77911419cc056337db6f8b0990d354a1781fe06f7a63f46bce8e0e",
        "electrical_engineering:ieee_c37_102_2023": "6be5dc22c93c9c582ad84fa79c6a3cd89c3716bbb71d10f216dd6d0cd13294ae",
        "electrical_engineering:ieee_c37_91_2021": "95ca7f323a05ad328c6dc0a87c6a2ab1c7f632c4da783abdb21203a4ccad1987",
        "electrical_engineering:infineon_server_rack_power_management": "9b93f8c23ca1cbcfa45e55e91d67f9cdf35b16321c9a3d5ef52ae35d00fcc8e5",
        "electrical_engineering:schneider_i_line_busway": "2adc16110fb50f76e6d95602a7456acc72dfec453b1f6c506c815341f138abf5",
        "electrical_engineering:schneider_medium_voltage_unit_substations": "2e9c4d5e2581bf718e1abcd11621d0c1e3d03fe8e0de947121946e6a6aea6a56",
        "electrical_engineering:schneider_power_zone_4": "a4c2caabc54246653f25aa4f0a4575bbf4439c404b4bd92291634a9cf1a4db99",
        "electrical_engineering:sel_transformer_protection_application": "820a8c6cc6599971ea25e0bfc4d73e225c5cba9440ef1bfb73000959f38d68a7",
        "electrical_engineering:ti_multiphase_processor_core_power": "9fe96b82a81fadc725398a5d0e49f6cbe7641da1a20daa207ff6792e1701502c",
        "electrical_engineering:vertiv_ups_bess_roles": "cd7ecd3f8fb0adf7f1a2794d9cffe8e746fa883849ef0059f3be5ad45d6f3fae",
        "thermal_engineering:doe_femp_best_practices_2024": "f6370789699da59a76b2d6a074aab178d7a29c844061e9dc6b7fa0f46187f8fe",
        "thermal_engineering:doe_femp_cooling_water_2019": "40c403bdc4b3ddc9e12dbd01fda6f983be99ce2d8f8c2504ce90dd5bbc8dd1fe",
        "thermal_engineering:doe_pnnl_data_center_emt_2025": "518dd70714a9dcc57fbab135440ac324751719eeeafca17823977345f64897f3",
        "thermal_engineering:ocp_cold_plate_requirements": "707568f722b6f26f92fb4ad48ae6aec8f1326fc7a9b19003eba220278e7831b8",
        "thermal_engineering:ocp_liquid_to_liquid_cdu_2024": "beb67767a05a80050bb612f1299118c18a3f22cafa7a55ce1d30a7c40b24d7be",
    }
)
SUBJECT_REQUIRED_FIELDS = {"id", "canonical_name"}
SUBJECT_FIELDS = SUBJECT_REQUIRED_FIELDS | {
    "applicability",
    "atlas_stable_key",
    "location",
    "scope",
}
EVIDENCE_BOUNDARY_REQUIRED_FIELDS = {"included_scope", "excluded_scope"}
EVIDENCE_BOUNDARY_FIELDS = EVIDENCE_BOUNDARY_REQUIRED_FIELDS | {
    "availability_rule",
    "capacity_rule",
    "promotion_rule",
}
LEDGER_CONTEXT_FIELDS = (
    "schema_version",
    "subject",
    "accessed_as_of",
    "evidence_boundary",
)
LEDGER_CONTEXT_CONTRACT = MappingProxyType(
    {
        "abilene": "1c1494827e6e8cc56cc07d5b04ddf683a0eaa23a4cf2498e00f4661b71e333c9",
        "abilene_execution": "1b301997111b6740fbcf56906c49faa42158348af8d5e962f0b82d3d962cc902",
        "commercial_compute": "bf986a8c04137b5bcbbb491e28688f32e389a46fa3331b57f587ed60ed0ecca3",
        "commercial_energy": "f5184d6f61aea7a9c81b379f2b0eb9dd2665f9a3b217ba92b68fec61f5c054d3",
        "delivery_resilience": "24b94602d3354507bda82b30aa502b5c93862ce776a1896cbfa3ca69f5ffdb87",
        "electrical_engineering": "d5f32f8f4ec2d02d13b48eeb6905648307790b718451a654b23f232acf7fbccc",
        "thermal_engineering": "ede7b686af98b6137b10aab50ce08522bf3dd004bdfe86916ed18a8e7d71d509",
    }
)
LIFECYCLES = set(layout_pipeline.LIFECYCLE_STYLE)
FACT_POSTURES = {
    "authoritative_guidance",
    "anticipated_not_observed",
    "confirmed",
    "confirmed_contract",
    "confirmed_minimum",
    "confirmed_model_spec",
    "design_not_as_built",
    "design_not_observed",
    "design_selected",
    "derived_from_authoritative_sources",
    "excluded_scope",
    "future_design",
    "live_by_not_start_date",
    "model_range_not_site_configured",
    "no_evidence_backed_estimate",
    "permitted_not_observed",
    "planned_not_operational",
    "reported_untyped",
    "unverified_null",
}
FACT_LIFECYCLES = {
    "accounting_standard",
    "announced_structure",
    "anticipated_maintenance",
    "as_built_unknown",
    "benchmark_method",
    "commissioning_unknown",
    "constructed",
    "contracted",
    "contracted_structure",
    "contract_term_unknown",
    "counterparty_unknown",
    "delivered_untyped",
    "deployed",
    "design_ceiling",
    "design_reference",
    "design_requirement",
    "energized",
    "future_design",
    "financing_terms_unknown",
    "installation_unknown",
    "operating",
    "operating_business_model",
    "operation_unknown",
    "ownership_unknown",
    "permitted",
    "planned",
    "product_documented",
    "published_method",
    "review_design",
    "derived_scenario_method",
    "selected_design",
    "site_configuration_unknown",
    "topology_unknown",
}
OPERATIONAL_MASTER_LIFECYCLES = {"energized", "operational_confirmed"}
OPERATIONAL_FACT_LIFECYCLES = {"energized", "operating", "deployed"}
OPERATIONAL_ALLOWED_FACT_LIFECYCLES = OPERATIONAL_FACT_LIFECYCLES | {"constructed"}
EMPTY_FACT_IDS_ALLOWED = {"conceptual", "course_variant", "terminal"}
DESIGN_FACT_LIFECYCLES = {
    "anticipated_maintenance",
    "design_ceiling",
    "design_reference",
    "design_requirement",
    "future_design",
    "review_design",
    "selected_design",
}
NULL_POSTURES = {"no_evidence_backed_estimate", "unverified_null"}
NUMERIC_FACT_UNITS = {
    "GPUs",
    "GPUs per building",
    "MW",
    "MW approximate customer-side load reduction",
    "VAC",
    "accelerators",
    "buildings",
    "dimensionless ratio",
    "fraction of IT power",
    "ft",
    "gallons",
    "gallons per building",
    "gallons per building per year",
    "kV",
    "main power transformers",
    "model FLOPs utilization fraction",
    "output tokens per second",
    "per unit per second for approximately 250 milliseconds",
    "percent",
    "units",
    "utilization fraction",
    "years",
}
BOOLEAN_FACT_UNITS = {"boolean"}
TEXT_FACT_UNITS = {
    None,
    "CDU configuration",
    "GE Vernova portfolio availability",
    "ISO-8601 date",
    "ISO-8601 date upper bound",
    "ISO-8601 month",
    "ISO-8601 month-end bound",
    "ISO-8601 year-end bound",
    "VDC",
    "accounting boundary",
    "air-cooling configuration",
    "announced project role",
    "assumption-driven scenario recipe",
    "authoritative energy-accounting definition",
    "benchmark measurement boundary",
    "board-level electrical configuration",
    "commissioning-stage sequence",
    "component path",
    "component set",
    "configuration dependency",
    "contractual milestone schedule",
    "contractual risk allocation",
    "cooling topology",
    "customer-specific interconnection status",
    "debt-equity and cash-flow allocation",
    "delivery-stage sequence",
    "derived training scenario rule",
    "electrical topology and state",
    "equipment financing structure",
    "first global shipment month",
    "generic architectural distinction",
    "generic ride-through role",
    "installed equipment family",
    "kV AC",
    "legal owner",
    "load-dynamics relationship",
    "manufacturer product configuration",
    "model and unit-count configuration",
    "model and workload specification",
    "months",
    "named asset and operating boundary",
    "named business-model comparison",
    "named compute delivery and workload roles",
    "named contract comparison",
    "named initial equity funders",
    "named lease posture",
    "named project role",
    "named risk-allocation comparison",
    "named tenant",
    "named transaction structure",
    "named utility construction project",
    "operating status",
    "operator-observed load pattern",
    "owner by asset class",
    "percent reduction in fluctuation magnitude in Google's test case",
    "platform design reference",
    "platform family",
    "program-level responsibility allocation",
    "project-delivery relationship",
    "protection configuration",
    "published training-method boundary",
    "rack configuration",
    "response-time relationship",
    "review-drawing status",
    "runtime configuration",
    "runtime performance dependency",
    "scenario calculation rule",
    "second",
    "selected facility-cooling design",
    "selected heat-rejection equipment family",
    "selected operating role",
    "selected piping materials",
    "site execution milestone",
    "site-level active-power waveform",
    "site-specific evidence bundle",
    "status",
    "system design",
    "temperatures, flow, pressure, and thermal capacity",
    "topology",
    "topology reference",
    "training-efficiency definition",
    "transformer configuration",
    "utility interconnection project scope",
    "weeks",
}
FACT_UNIT_VALUE_KIND = {
    **{unit: "number" for unit in NUMERIC_FACT_UNITS},
    **{unit: "boolean" for unit in BOOLEAN_FACT_UNITS},
    **{unit: "text" for unit in TEXT_FACT_UNITS},
}
FACT_IDENTITY_CONTRACT = MappingProxyType(
    {
        "abilene:adjacent_microsoft_planned_buildings": ("buildings", "number"),
        "abilene:adjacent_microsoft_planned_capacity_mw": ("MW", "number"),
        "abilene:adjacent_microsoft_scope_included": ("boolean", "boolean"),
        "abilene:bess_campus_connection_as_built_topology": ("topology", "text"),
        "abilene:bess_operational_status": ("status", "text"),
        "abilene:bess_reference_design_status": ("status", "text"),
        "abilene:buildings_energized_confirmed_min": ("buildings", "number"),
        "abilene:campus_lpt_secondary_as_built_voltage_kv": ("kV", "number"),
        "abilene:campus_mv_reference_design_voltage_kv": ("kV", "number"),
        "abilene:campus_planned_buildings": ("buildings", "number"),
        "abilene:campus_source_merge_as_built_topology": ("topology", "text"),
        "abilene:cooling_annual_maintenance_gallons_per_building": (
            "gallons per building per year",
            "number",
        ),
        "abilene:cooling_direct_to_chip_design": ("system design", "text"),
        "abilene:cooling_heat_rejection_posture": ("system design", "text"),
        "abilene:cooling_initial_fill_gallons_per_building": (
            "gallons per building",
            "number",
        ),
        "abilene:cooling_measured_operating_consumption_gallons": ("gallons", "number"),
        "abilene:diesel_campus_connection_as_built_topology": ("topology", "text"),
        "abilene:diesel_operational_units": ("units", "number"),
        "abilene:diesel_permitted_nameplate_mw": ("MW", "number"),
        "abilene:diesel_units_authorized": ("units", "number"),
        "abilene:diesel_units_installed": ("units", "number"),
        "abilene:early_training_inference_live_by": ("ISO-8601 date", "text"),
        "abilene:exact_workload_start_date": ("ISO-8601 date", "text"),
        "abilene:gas_commissioned_mw": ("MW", "number"),
        "abilene:gas_permitted_nameplate_mw": ("MW", "number"),
        "abilene:gas_turbine_units_authorized": ("units", "number"),
        "abilene:generator_terminal_model_voltage_range_kv": ("kV AC", "text"),
        "abilene:generator_terminal_site_voltage_kv": ("kV AC", "text"),
        "abilene:gpu_design_ceiling_per_building": ("GPUs per building", "number"),
        "abilene:grid_expansion_fully_energized_by": ("ISO-8601 date", "text"),
        "abilene:grid_expansion_substation_capacity_mw": ("MW", "number"),
        "abilene:grid_expansion_substation_voltage_kv": ("kV", "number"),
        "abilene:grid_expansion_transformers_energized_count": (
            "main power transformers",
            "number",
        ),
        "abilene:grid_expansion_upstream_line": (None, "text"),
        "abilene:grid_initial_service_operational_as_of": ("ISO-8601 date", "text"),
        "abilene:grid_initial_slack_span_length_ft": ("ft", "number"),
        "abilene:grid_initial_source_line": (None, "text"),
        "abilene:grid_initial_substation_capacity_mw": ("MW", "number"),
        "abilene:grid_initial_substation_voltage_kv": ("kV", "number"),
        "abilene:installed_gpu_count": ("GPUs", "number"),
        "abilene:operational_buildings_exact": ("buildings", "number"),
        "abilene:oracle_capacity_delivered_percent_untyped": ("percent", "number"),
        "abilene:planned_grid_interconnection_mw": ("MW", "number"),
        "abilene:rack_air_cooled_components": ("component set", "text"),
        "abilene:rack_liquid_cooled_components": ("component path", "text"),
        "abilene:rack_platform": ("platform family", "text"),
        "abilene:rack_platform_nvl72_design_reference": (
            "platform design reference",
            "text",
        ),
        "abilene:rack_power_shelf_ac_input_voltage_v": ("VAC", "number"),
        "abilene:rack_power_shelf_output_vdc": ("VDC", "text"),
        "abilene_execution:building_electrical_delivery_scope": (
            "site execution milestone",
            "text",
        ),
        "abilene_execution:building_power_train_as_built_configuration": (
            "electrical topology and state",
            "text",
        ),
        "abilene_execution:campus_construction_start_month": ("ISO-8601 month", "text"),
        "abilene_execution:cdu_site_configuration": ("CDU configuration", "text"),
        "abilene_execution:contracted_grid_service_capacity_mw": ("MW", "number"),
        "abilene_execution:current_critical_it_load_mw": ("MW", "number"),
        "abilene_execution:current_operational_building_count_exact": (
            "buildings",
            "number",
        ),
        "abilene_execution:current_total_facility_load_mw": ("MW", "number"),
        "abilene_execution:early_training_and_inference_live_by": (
            "ISO-8601 date upper bound",
            "text",
        ),
        "abilene_execution:expansion_345_line_finish_date_as_reported": (
            "ISO-8601 date",
            "text",
        ),
        "abilene_execution:expansion_345_line_start_date_as_reported": (
            "ISO-8601 date",
            "text",
        ),
        "abilene_execution:expansion_345_named_line_project": (
            "named utility construction project",
            "text",
        ),
        "abilene_execution:expansion_permanent_transformer_swaps_expected_by": (
            "ISO-8601 month-end bound",
            "text",
        ),
        "abilene_execution:expansion_substation_all_five_transformers_energized_date": (
            "ISO-8601 date",
            "text",
        ),
        "abilene_execution:expansion_substation_first_transformer_energized_date": (
            "ISO-8601 date",
            "text",
        ),
        "abilene_execution:facility_cooling_interfaces_as_built": (
            "cooling topology",
            "text",
        ),
        "abilene_execution:facility_cooling_operating_measurements": (
            "temperatures, flow, pressure, and thermal capacity",
            "text",
        ),
        "abilene_execution:facility_cooling_pipe_materials": (
            "selected piping materials",
            "text",
        ),
        "abilene_execution:facility_cooling_water_system_design": (
            "selected facility-cooling design",
            "text",
        ),
        "abilene_execution:facility_heat_rejection_terminal": (
            "selected heat-rejection equipment family",
            "text",
        ),
        "abilene_execution:first_phase_operational_by": (
            "ISO-8601 date upper bound",
            "text",
        ),
        "abilene_execution:first_two_buildings_energized_by": (
            "ISO-8601 date upper bound",
            "text",
        ),
        "abilene_execution:gas_turbine_commissioned_capacity_mw": ("MW", "number"),
        "abilene_execution:gas_turbine_current_operating_posture": (
            "operating status",
            "text",
        ),
        "abilene_execution:gas_turbine_current_output_mw": ("MW", "number"),
        "abilene_execution:gb200_first_rack_delivery_month": ("ISO-8601 month", "text"),
        "abilene_execution:ge_vernovas_gas_turbines_installed": (
            "installed equipment family",
            "text",
        ),
        "abilene_execution:generator_gsu_protection_as_built": (
            "protection configuration",
            "text",
        ),
        "abilene_execution:generator_terminal_site_voltage_kv": ("kV AC", "text"),
        "abilene_execution:gsu_as_built_ratio_and_connection": (
            "transformer configuration",
            "text",
        ),
        "abilene_execution:initial_aep_poi_energized_date": ("ISO-8601 date", "text"),
        "abilene_execution:initial_aep_poi_scope": (
            "utility interconnection project scope",
            "text",
        ),
        "abilene_execution:initial_aep_terminal_energized_date": (
            "ISO-8601 date",
            "text",
        ),
        "abilene_execution:initial_aep_terminal_equipment_scope": (
            "utility interconnection project scope",
            "text",
        ),
        "abilene_execution:installed_gas_turbine_intended_role": (
            "selected operating role",
            "text",
        ),
        "abilene_execution:installed_gas_turbine_model_mix": (
            "model and unit-count configuration",
            "text",
        ),
        "abilene_execution:installed_gas_turbine_unit_count": ("units", "number"),
        "abilene_execution:onsite_power_plant_delivery_confirmed": (
            "site execution milestone",
            "text",
        ),
        "abilene_execution:operating_rack_configuration": (
            "rack configuration",
            "text",
        ),
        "abilene_execution:original_remaining_six_buildings_planned_completion": (
            "ISO-8601 year-end bound",
            "text",
        ),
        "abilene_execution:rack_site_core_voltage": (
            "board-level electrical configuration",
            "text",
        ),
        "abilene_execution:residual_air_site_configuration": (
            "air-cooling configuration",
            "text",
        ),
        "abilene_execution:site_specific_interconnection_queue_and_contract_record": (
            "customer-specific interconnection status",
            "text",
        ),
        "commercial_energy:crane_microsoft_ppa_contract": (
            "named contract comparison",
            "text",
        ),
        "commercial_energy:scope2_contractual_attributes_not_physical_flow": (
            "accounting boundary",
            "text",
        ),
        "commercial_compute:abilene_2024_crusoe_owner_developer_announcement": (
            "announced project role",
            "text",
        ),
        "commercial_compute:abilene_accelerator_active_utilization": (
            "utilization fraction",
            "number",
        ),
        "commercial_compute:abilene_accelerator_power_share": (
            "fraction of IT power",
            "number",
        ),
        "commercial_compute:abilene_capital_stack_waterfall": (
            "debt-equity and cash-flow allocation",
            "text",
        ),
        "commercial_compute:abilene_compute_activity_roles": (
            "named compute delivery and workload roles",
            "text",
        ),
        "commercial_compute:abilene_current_facility_power_mw": ("MW", "number"),
        "commercial_compute:abilene_current_it_power_mw": ("MW", "number"),
        "commercial_compute:abilene_current_pue": ("dimensionless ratio", "number"),
        "commercial_compute:abilene_inference_batching_configuration": (
            "runtime configuration",
            "text",
        ),
        "commercial_compute:abilene_installed_accelerator_count": (
            "accelerators",
            "number",
        ),
        "commercial_compute:abilene_it_equipment_financing_terms": (
            "equipment financing structure",
            "text",
        ),
        "commercial_compute:abilene_it_equipment_legal_owner": ("legal owner", "text"),
        "commercial_compute:abilene_lancium_development_role": (
            "announced project role",
            "text",
        ),
        "commercial_compute:abilene_land_legal_owner": ("legal owner", "text"),
        "commercial_compute:abilene_measured_token_throughput": (
            "output tokens per second",
            "number",
        ),
        "commercial_compute:abilene_model_and_workload_configuration": (
            "model and workload specification",
            "text",
        ),
        "commercial_compute:abilene_phase1_crusoe_delivery_and_operations_role": (
            "named project role",
            "text",
        ),
        "commercial_compute:abilene_phase1_financing_structure": (
            "named transaction structure",
            "text",
        ),
        "commercial_compute:abilene_phase1_lease_structure": (
            "named lease posture",
            "text",
        ),
        "commercial_compute:abilene_phase1_lease_term_years": ("years", "number"),
        "commercial_compute:abilene_phase1_tenant_identity": ("named tenant", "text"),
        "commercial_compute:abilene_phase2_financing_structure": (
            "named transaction structure",
            "text",
        ),
        "commercial_compute:abilene_power_asset_ownership_by_component": (
            "owner by asset class",
            "text",
        ),
        "commercial_compute:abilene_rent_commencement_and_acceptance_terms": (
            "contractual milestone schedule",
            "text",
        ),
        "commercial_compute:abilene_training_mfu": (
            "model FLOPs utilization fraction",
            "number",
        ),
        "commercial_compute:abilene_usable_accelerator_power_mw": ("MW", "number"),
        "commercial_compute:abilene_utilization_risk_allocation": (
            "contractual risk allocation",
            "text",
        ),
        "commercial_compute:coreweave_ai_cloud_contract_and_financing_comparison": (
            "named business-model comparison",
            "text",
        ),
        "commercial_compute:coreweave_capacity_and_utilization_risk_comparison": (
            "named risk-allocation comparison",
            "text",
        ),
        "commercial_compute:coreweave_facility_and_equipment_boundary_comparison": (
            "named asset and operating boundary",
            "text",
        ),
        "commercial_compute:dense_decoder_training_flops_per_token_method": (
            "published training-method boundary",
            "text",
        ),
        "commercial_compute:dense_decoder_training_tokens_recipe": (
            "derived training scenario rule",
            "text",
        ),
        "commercial_compute:dgx_gb_nvl72_product_reference": (
            "manufacturer product configuration",
            "text",
        ),
        "commercial_compute:equinix_asset_and_operating_boundary": (
            "named asset and operating boundary",
            "text",
        ),
        "commercial_compute:equinix_colocation_comparison": (
            "named business-model comparison",
            "text",
        ),
        "commercial_compute:facility_energy_to_it_energy_recipe": (
            "scenario calculation rule",
            "text",
        ),
        "commercial_compute:inference_batching_dependency": (
            "runtime performance dependency",
            "text",
        ),
        "commercial_compute:inference_measurement_boundary": (
            "benchmark measurement boundary",
            "text",
        ),
        "commercial_compute:inference_tokens_recipe": (
            "scenario calculation rule",
            "text",
        ),
        "commercial_compute:microsoft_hyperscale_cloud_comparison": (
            "named business-model comparison",
            "text",
        ),
        "commercial_compute:mw_to_tokens_scenario_recipe": (
            "assumption-driven scenario recipe",
            "text",
        ),
        "commercial_compute:pue_energy_boundary": (
            "authoritative energy-accounting definition",
            "text",
        ),
        "commercial_compute:stargate_initial_equity_funders": (
            "named initial equity funders",
            "text",
        ),
        "commercial_compute:stargate_lead_responsibility_split": (
            "program-level responsibility allocation",
            "text",
        ),
        "commercial_compute:training_mfu_definition": (
            "training-efficiency definition",
            "text",
        ),
        "delivery_resilience:abilene_bess_function_rating_connection_operation": (
            "site-specific evidence bundle",
            "text",
        ),
        "delivery_resilience:abilene_bess_reference_design_status": (
            "review-drawing status",
            "text",
        ),
        "delivery_resilience:abilene_operating_transient_profile": (
            "site-level active-power waveform",
            "text",
        ),
        "delivery_resilience:ai_training_checkpoint_transition_duration": (
            "second",
            "text",
        ),
        "delivery_resilience:ai_training_observed_ramp_rate": (
            "per unit per second for approximately 250 milliseconds",
            "number",
        ),
        "delivery_resilience:gas_turbine_slot_can_precede_site_readiness": (
            "project-delivery relationship",
            "text",
        ),
        "delivery_resilience:ge_gas_turbine_delivery_slot_exposure_2025": (
            "GE Vernova portfolio availability",
            "text",
        ),
        "delivery_resilience:google_compiler_power_shaping_result": (
            "percent reduction in fluctuation magnitude in Google's test case",
            "text",
        ),
        "delivery_resilience:google_synchronized_ml_fluctuation_observation": (
            "operator-observed load pattern",
            "text",
        ),
        "delivery_resilience:large_load_grid_response_mismatch": (
            "response-time relationship",
            "text",
        ),
        "delivery_resilience:large_power_transformer_delivery_chain": (
            "delivery-stage sequence",
            "text",
        ),
        "delivery_resilience:liquid_cooling_acceptance_sequence": (
            "commissioning-stage sequence",
            "text",
        ),
        "delivery_resilience:parallel_ai_load_correlation": (
            "load-dynamics relationship",
            "text",
        ),
        "delivery_resilience:standardized_row_cooling_lead_time_2026": (
            "weeks",
            "text",
        ),
        "delivery_resilience:uniflair_xca_initial_shipping_date": (
            "first global shipment month",
            "text",
        ),
        "delivery_resilience:ups_and_btm_bess_role_separation": (
            "generic architectural distinction",
            "text",
        ),
        "delivery_resilience:ups_ridethrough_depends_on_site_settings": (
            "configuration dependency",
            "text",
        ),
        "delivery_resilience:ups_short_duration_ride_through_role": (
            "generic ride-through role",
            "text",
        ),
        "delivery_resilience:us_distribution_transformer_lead_time_2023": (
            "months",
            "text",
        ),
        "delivery_resilience:us_large_power_transformer_lead_time_2024": (
            "months",
            "text",
        ),
        "delivery_resilience:voltage_sag_data_center_load_loss_event": (
            "MW approximate customer-side load reduction",
            "number",
        ),
        "electrical_engineering:busway_feeder_and_plugin_distribution_role": (
            None,
            "text",
        ),
        "electrical_engineering:generator_protection_fault_scope": (None, "text"),
        "electrical_engineering:generator_rotor_to_electricity_conversion": (
            None,
            "text",
        ),
        "electrical_engineering:gsu_generator_to_network_voltage_function": (
            None,
            "text",
        ),
        "electrical_engineering:gsu_protection_zone_application_specificity": (
            None,
            "text",
        ),
        "electrical_engineering:low_voltage_switchgear_distribution_protection_role": (
            None,
            "text",
        ),
        "electrical_engineering:multiphase_processor_core_power_role": (None, "text"),
        "electrical_engineering:transformer_protection_engineering_scope": (
            None,
            "text",
        ),
        "electrical_engineering:turbine_fluid_to_rotor_conversion": (None, "text"),
        "electrical_engineering:unit_substation_coordinated_assembly_role": (
            None,
            "text",
        ),
        "electrical_engineering:ups_conditioned_no_break_power_role": (None, "text"),
        "electrical_engineering:vrm_intermediate_bus_to_xpu_voltage_role": (
            None,
            "text",
        ),
        "electrical_engineering:xpu_low_voltage_high_current_requirement": (
            None,
            "text",
        ),
        "thermal_engineering:generic_cdu_control_functions": (None, "text"),
        "thermal_engineering:generic_cdu_loop_isolation_heat_exchange": (
            "topology reference",
            "text",
        ),
        "thermal_engineering:generic_cold_plate_heat_transfer": (None, "text"),
        "thermal_engineering:generic_crah_air_heat_removal_path": (
            "topology reference",
            "text",
        ),
        "thermal_engineering:generic_crah_variable_airflow_control": (None, "text"),
        "thermal_engineering:generic_facility_loop_heat_transport": (
            "topology reference",
            "text",
        ),
        "thermal_engineering:generic_facility_loop_load_control": (None, "text"),
        "thermal_engineering:generic_ite_electrical_input_heat": (None, "text"),
        "thermal_engineering:generic_parallel_liquid_air_cooling": (
            "topology reference",
            "text",
        ),
        "thermal_engineering:generic_rack_manifold_flow_role": (None, "text"),
        "thermal_engineering:generic_tcs_supply_return_path": (
            "topology reference",
            "text",
        ),
    }
)
FACT_SEMANTIC_CONTRACT = MappingProxyType(
    {
        qualified_id: (value_is_null, posture, lifecycle)
        for value_is_null, posture, lifecycle, qualified_ids in (
            (
                False,
                "anticipated_not_observed",
                "anticipated_maintenance",
                ("abilene:cooling_annual_maintenance_gallons_per_building",),
            ),
            (
                False,
                "authoritative_guidance",
                "accounting_standard",
                (
                    "commercial_compute:pue_energy_boundary",
                    "commercial_energy:scope2_contractual_attributes_not_physical_flow",
                ),
            ),
            (
                False,
                "authoritative_guidance",
                "benchmark_method",
                ("commercial_compute:inference_measurement_boundary",),
            ),
            (
                False,
                "authoritative_guidance",
                "product_documented",
                ("commercial_compute:inference_batching_dependency",),
            ),
            (
                False,
                "authoritative_guidance",
                "published_method",
                (
                    "commercial_compute:dense_decoder_training_flops_per_token_method",
                    "commercial_compute:training_mfu_definition",
                ),
            ),
            (
                False,
                "confirmed",
                "announced_structure",
                (
                    "commercial_compute:abilene_2024_crusoe_owner_developer_announcement",
                    "commercial_compute:abilene_lancium_development_role",
                    "commercial_compute:stargate_initial_equity_funders",
                    "commercial_compute:stargate_lead_responsibility_split",
                ),
            ),
            (
                False,
                "confirmed",
                "constructed",
                (
                    "abilene:grid_initial_slack_span_length_ft",
                    "abilene:grid_initial_source_line",
                    "abilene:grid_initial_substation_capacity_mw",
                    "abilene:grid_initial_substation_voltage_kv",
                    "abilene_execution:building_electrical_delivery_scope",
                    "abilene_execution:campus_construction_start_month",
                    "abilene_execution:ge_vernovas_gas_turbines_installed",
                    "abilene_execution:onsite_power_plant_delivery_confirmed",
                ),
            ),
            (
                False,
                "confirmed",
                "deployed",
                (
                    "abilene:rack_platform",
                    "abilene_execution:gb200_first_rack_delivery_month",
                    "delivery_resilience:google_compiler_power_shaping_result",
                ),
            ),
            (
                False,
                "confirmed",
                "energized",
                (
                    "abilene:grid_expansion_fully_energized_by",
                    "abilene:grid_expansion_substation_capacity_mw",
                    "abilene:grid_expansion_substation_voltage_kv",
                    "abilene:grid_expansion_transformers_energized_count",
                    "abilene_execution:expansion_substation_all_five_transformers_energized_date",
                    "abilene_execution:expansion_substation_first_transformer_energized_date",
                    "abilene_execution:first_two_buildings_energized_by",
                    "abilene_execution:initial_aep_poi_energized_date",
                    "abilene_execution:initial_aep_poi_scope",
                    "abilene_execution:initial_aep_terminal_energized_date",
                    "abilene_execution:initial_aep_terminal_equipment_scope",
                ),
            ),
            (
                False,
                "confirmed",
                "operating",
                (
                    "abilene:grid_initial_service_operational_as_of",
                    "abilene_execution:first_phase_operational_by",
                    "commercial_compute:abilene_compute_activity_roles",
                    "delivery_resilience:google_synchronized_ml_fluctuation_observation",
                ),
            ),
            (
                False,
                "confirmed",
                "operating_business_model",
                (
                    "commercial_compute:coreweave_ai_cloud_contract_and_financing_comparison",
                    "commercial_compute:coreweave_facility_and_equipment_boundary_comparison",
                    "commercial_compute:equinix_asset_and_operating_boundary",
                    "commercial_compute:equinix_colocation_comparison",
                    "commercial_compute:microsoft_hyperscale_cloud_comparison",
                ),
            ),
            (
                False,
                "confirmed",
                "planned",
                ("abilene:campus_planned_buildings",),
            ),
            (
                False,
                "confirmed_contract",
                "contracted",
                ("commercial_energy:crane_microsoft_ppa_contract",),
            ),
            (
                False,
                "confirmed_contract",
                "contracted_structure",
                (
                    "commercial_compute:abilene_phase1_crusoe_delivery_and_operations_role",
                    "commercial_compute:abilene_phase1_financing_structure",
                    "commercial_compute:abilene_phase1_lease_structure",
                    "commercial_compute:abilene_phase2_financing_structure",
                ),
            ),
            (
                False,
                "confirmed_contract",
                "operating_business_model",
                (
                    "commercial_compute:coreweave_capacity_and_utilization_risk_comparison",
                ),
            ),
            (
                False,
                "confirmed_minimum",
                "energized",
                ("abilene:buildings_energized_confirmed_min",),
            ),
            (
                False,
                "confirmed_model_spec",
                "product_documented",
                (
                    "abilene:rack_air_cooled_components",
                    "abilene:rack_liquid_cooled_components",
                    "abilene:rack_power_shelf_output_vdc",
                    "commercial_compute:dgx_gb_nvl72_product_reference",
                    "delivery_resilience:ge_gas_turbine_delivery_slot_exposure_2025",
                    "delivery_resilience:standardized_row_cooling_lead_time_2026",
                    "delivery_resilience:uniflair_xca_initial_shipping_date",
                    "electrical_engineering:busway_feeder_and_plugin_distribution_role",
                    "electrical_engineering:gsu_generator_to_network_voltage_function",
                    "electrical_engineering:low_voltage_switchgear_distribution_protection_role",
                    "electrical_engineering:multiphase_processor_core_power_role",
                    "electrical_engineering:unit_substation_coordinated_assembly_role",
                    "electrical_engineering:vrm_intermediate_bus_to_xpu_voltage_role",
                    "electrical_engineering:xpu_low_voltage_high_current_requirement",
                ),
            ),
            (
                False,
                "derived_from_authoritative_sources",
                "derived_scenario_method",
                (
                    "commercial_compute:dense_decoder_training_tokens_recipe",
                    "commercial_compute:facility_energy_to_it_energy_recipe",
                    "commercial_compute:inference_tokens_recipe",
                    "commercial_compute:mw_to_tokens_scenario_recipe",
                ),
            ),
            (
                False,
                "design_not_as_built",
                "review_design",
                ("abilene:campus_mv_reference_design_voltage_kv",),
            ),
            (
                False,
                "design_not_observed",
                "design_ceiling",
                ("abilene:gpu_design_ceiling_per_building",),
            ),
            (
                False,
                "design_not_observed",
                "design_reference",
                (
                    "abilene:cooling_direct_to_chip_design",
                    "abilene:rack_platform_nvl72_design_reference",
                    "delivery_resilience:ai_training_checkpoint_transition_duration",
                    "delivery_resilience:ai_training_observed_ramp_rate",
                    "delivery_resilience:gas_turbine_slot_can_precede_site_readiness",
                    "delivery_resilience:large_load_grid_response_mismatch",
                    "delivery_resilience:large_power_transformer_delivery_chain",
                    "delivery_resilience:liquid_cooling_acceptance_sequence",
                    "delivery_resilience:parallel_ai_load_correlation",
                    "delivery_resilience:ups_and_btm_bess_role_separation",
                    "delivery_resilience:ups_ridethrough_depends_on_site_settings",
                    "delivery_resilience:ups_short_duration_ride_through_role",
                    "delivery_resilience:us_distribution_transformer_lead_time_2023",
                    "delivery_resilience:us_large_power_transformer_lead_time_2024",
                    "delivery_resilience:voltage_sag_data_center_load_loss_event",
                    "electrical_engineering:generator_protection_fault_scope",
                    "electrical_engineering:generator_rotor_to_electricity_conversion",
                    "electrical_engineering:gsu_protection_zone_application_specificity",
                    "electrical_engineering:transformer_protection_engineering_scope",
                    "electrical_engineering:turbine_fluid_to_rotor_conversion",
                    "electrical_engineering:ups_conditioned_no_break_power_role",
                    "thermal_engineering:generic_cdu_control_functions",
                    "thermal_engineering:generic_cdu_loop_isolation_heat_exchange",
                    "thermal_engineering:generic_cold_plate_heat_transfer",
                    "thermal_engineering:generic_crah_air_heat_removal_path",
                    "thermal_engineering:generic_crah_variable_airflow_control",
                    "thermal_engineering:generic_facility_loop_heat_transport",
                    "thermal_engineering:generic_facility_loop_load_control",
                    "thermal_engineering:generic_ite_electrical_input_heat",
                    "thermal_engineering:generic_parallel_liquid_air_cooling",
                    "thermal_engineering:generic_rack_manifold_flow_role",
                    "thermal_engineering:generic_tcs_supply_return_path",
                ),
            ),
            (
                False,
                "design_selected",
                "design_requirement",
                ("abilene:cooling_initial_fill_gallons_per_building",),
            ),
            (
                False,
                "design_selected",
                "selected_design",
                (
                    "abilene:cooling_heat_rejection_posture",
                    "abilene_execution:facility_cooling_pipe_materials",
                    "abilene_execution:facility_cooling_water_system_design",
                    "abilene_execution:facility_heat_rejection_terminal",
                    "abilene_execution:installed_gas_turbine_intended_role",
                ),
            ),
            (
                False,
                "excluded_scope",
                "planned",
                (
                    "abilene:adjacent_microsoft_planned_buildings",
                    "abilene:adjacent_microsoft_planned_capacity_mw",
                    "abilene:adjacent_microsoft_scope_included",
                ),
            ),
            (
                False,
                "future_design",
                "future_design",
                (
                    "abilene:bess_reference_design_status",
                    "delivery_resilience:abilene_bess_reference_design_status",
                ),
            ),
            (
                False,
                "live_by_not_start_date",
                "operating",
                (
                    "abilene:early_training_inference_live_by",
                    "abilene_execution:early_training_and_inference_live_by",
                ),
            ),
            (
                False,
                "model_range_not_site_configured",
                "product_documented",
                ("abilene:generator_terminal_model_voltage_range_kv",),
            ),
            (
                False,
                "permitted_not_observed",
                "permitted",
                (
                    "abilene:diesel_permitted_nameplate_mw",
                    "abilene:diesel_units_authorized",
                    "abilene:gas_permitted_nameplate_mw",
                    "abilene:gas_turbine_units_authorized",
                ),
            ),
            (
                False,
                "planned_not_operational",
                "planned",
                (
                    "abilene:planned_grid_interconnection_mw",
                    "abilene_execution:expansion_345_line_finish_date_as_reported",
                    "abilene_execution:expansion_345_line_start_date_as_reported",
                    "abilene_execution:expansion_345_named_line_project",
                    "abilene_execution:expansion_permanent_transformer_swaps_expected_by",
                    "abilene_execution:original_remaining_six_buildings_planned_completion",
                ),
            ),
            (
                False,
                "reported_untyped",
                "delivered_untyped",
                ("abilene:oracle_capacity_delivered_percent_untyped",),
            ),
            (
                True,
                "no_evidence_backed_estimate",
                "operation_unknown",
                (
                    "abilene:installed_gpu_count",
                    "commercial_compute:abilene_accelerator_active_utilization",
                    "commercial_compute:abilene_accelerator_power_share",
                    "commercial_compute:abilene_current_facility_power_mw",
                    "commercial_compute:abilene_current_it_power_mw",
                    "commercial_compute:abilene_current_pue",
                    "commercial_compute:abilene_installed_accelerator_count",
                    "commercial_compute:abilene_measured_token_throughput",
                    "commercial_compute:abilene_training_mfu",
                    "commercial_compute:abilene_usable_accelerator_power_mw",
                ),
            ),
            (
                True,
                "unverified_null",
                "as_built_unknown",
                ("abilene:campus_lpt_secondary_as_built_voltage_kv",),
            ),
            (
                True,
                "unverified_null",
                "commissioning_unknown",
                (
                    "abilene:gas_commissioned_mw",
                    "abilene_execution:gas_turbine_commissioned_capacity_mw",
                ),
            ),
            (
                True,
                "unverified_null",
                "contract_term_unknown",
                (
                    "commercial_compute:abilene_phase1_lease_term_years",
                    "commercial_compute:abilene_rent_commencement_and_acceptance_terms",
                    "commercial_compute:abilene_utilization_risk_allocation",
                ),
            ),
            (
                True,
                "unverified_null",
                "counterparty_unknown",
                ("commercial_compute:abilene_phase1_tenant_identity",),
            ),
            (
                True,
                "unverified_null",
                "financing_terms_unknown",
                (
                    "commercial_compute:abilene_capital_stack_waterfall",
                    "commercial_compute:abilene_it_equipment_financing_terms",
                ),
            ),
            (
                True,
                "unverified_null",
                "installation_unknown",
                (
                    "abilene:diesel_units_installed",
                    "abilene_execution:installed_gas_turbine_model_mix",
                    "abilene_execution:installed_gas_turbine_unit_count",
                ),
            ),
            (
                True,
                "unverified_null",
                "operation_unknown",
                (
                    "abilene:bess_operational_status",
                    "abilene:cooling_measured_operating_consumption_gallons",
                    "abilene:diesel_operational_units",
                    "abilene:exact_workload_start_date",
                    "abilene:operational_buildings_exact",
                    "abilene_execution:current_critical_it_load_mw",
                    "abilene_execution:current_operational_building_count_exact",
                    "abilene_execution:current_total_facility_load_mw",
                    "abilene_execution:facility_cooling_operating_measurements",
                    "abilene_execution:gas_turbine_current_operating_posture",
                    "abilene_execution:gas_turbine_current_output_mw",
                    "commercial_compute:abilene_inference_batching_configuration",
                    "commercial_compute:abilene_model_and_workload_configuration",
                    "delivery_resilience:abilene_bess_function_rating_connection_operation",
                ),
            ),
            (
                True,
                "unverified_null",
                "ownership_unknown",
                (
                    "commercial_compute:abilene_it_equipment_legal_owner",
                    "commercial_compute:abilene_land_legal_owner",
                    "commercial_compute:abilene_power_asset_ownership_by_component",
                ),
            ),
            (
                True,
                "unverified_null",
                "site_configuration_unknown",
                (
                    "abilene:generator_terminal_site_voltage_kv",
                    "abilene:rack_power_shelf_ac_input_voltage_v",
                    "abilene_execution:cdu_site_configuration",
                    "abilene_execution:contracted_grid_service_capacity_mw",
                    "abilene_execution:generator_gsu_protection_as_built",
                    "abilene_execution:generator_terminal_site_voltage_kv",
                    "abilene_execution:operating_rack_configuration",
                    "abilene_execution:rack_site_core_voltage",
                    "abilene_execution:residual_air_site_configuration",
                    "abilene_execution:site_specific_interconnection_queue_and_contract_record",
                    "delivery_resilience:abilene_operating_transient_profile",
                ),
            ),
            (
                True,
                "unverified_null",
                "topology_unknown",
                (
                    "abilene:bess_campus_connection_as_built_topology",
                    "abilene:campus_source_merge_as_built_topology",
                    "abilene:diesel_campus_connection_as_built_topology",
                    "abilene:grid_expansion_upstream_line",
                    "abilene_execution:building_power_train_as_built_configuration",
                    "abilene_execution:facility_cooling_interfaces_as_built",
                    "abilene_execution:gsu_as_built_ratio_and_connection",
                ),
            ),
        )
        for qualified_id in qualified_ids
    }
)
FACT_NUMERIC_MINIMUM_CONTRACT = MappingProxyType(
    {
        qualified_id: 0
        for qualified_id, (_, kind) in FACT_IDENTITY_CONTRACT.items()
        if kind == "number"
    }
)
FACT_PAYLOAD_FIELDS = (
    "value",
    "unit",
    "scope",
    "basis",
    "source_ids",
    "lifecycle",
    "as_of",
    "posture",
)
FACT_PAYLOAD_CONTRACT = MappingProxyType(
    {
        "abilene:adjacent_microsoft_planned_buildings": "ec892f7577ed0fc4afcd57cf587e28701812e75382e171eecabcd339fbd86d96",
        "abilene:adjacent_microsoft_planned_capacity_mw": "cfc779500ac467b96eafe3af56109d48e4e22a12a9565b7423c7f470ff6a6e02",
        "abilene:adjacent_microsoft_scope_included": "496c1d6bc45d86f4b4c63cfe1c74879c1005f301b067d506a9cb3b5d2051aa15",
        "abilene:bess_campus_connection_as_built_topology": "6a4f51892389ecf2401bca1dd05c62a0e859cab7313776b6153c6ce1e553e661",
        "abilene:bess_operational_status": "1fcdb320a345599e1de38e62b10ff9e283926a899173695c9bf8cb63a634e54d",
        "abilene:bess_reference_design_status": "23ec286edfb021388301eb09c86e2bcf0f1f509aaf8324ff87c7f6eeb45dfaa5",
        "abilene:buildings_energized_confirmed_min": "e3b1f3434465b4955c0de7e1108a67bea796de8fbb85ae06fb7d8113c70089e9",
        "abilene:campus_lpt_secondary_as_built_voltage_kv": "4688eab915fb51224d2d1e888f0817e66a748b2ea80fae746ecab527aa8c7f6b",
        "abilene:campus_mv_reference_design_voltage_kv": "295d76943b2ccb2fe50446427ec3f776beaba7a96dc74328792e8128f29c52de",
        "abilene:campus_planned_buildings": "4da596133abb23e494a60604cb0f72f4c66d163fc099a4aece3ec433ad3095b2",
        "abilene:campus_source_merge_as_built_topology": "f144e458096c9b3d2fd6e33c8c0e65b5e9e8669b1c0e8d6be67a90ad6cea0eef",
        "abilene:cooling_annual_maintenance_gallons_per_building": "0cd23ec2b57a13653713a45e611866b1dfbbd7ba0d27a6d16f5ab2d6b8d88c36",
        "abilene:cooling_direct_to_chip_design": "20c8b29ca460c58ff21d09f66193a6e6252de5b10f1842d61736d630b529748a",
        "abilene:cooling_heat_rejection_posture": "c2ab25fa8daf2a87d94e5756faa5591779bc55d21aea73df73ffc1023e22aec1",
        "abilene:cooling_initial_fill_gallons_per_building": "de5660f83fab70e0592106bcf70e3187ced04c49a2130eba59cac680d866ceb2",
        "abilene:cooling_measured_operating_consumption_gallons": "4e4239d63f74dbfb6df2e430b0d7927e67794ac961e75a691b8daa4779d7ba90",
        "abilene:diesel_campus_connection_as_built_topology": "9dbf382cb08c5bb8cf6151f040ae5930d2b75fd3161ce82c44075e61539b6e46",
        "abilene:diesel_operational_units": "aa393268a88264768293212c6a2f9f1674c39fbedb11eb3c66211257489ba951",
        "abilene:diesel_permitted_nameplate_mw": "18a0a5c1150f400580618d3cbc67d9321dd696f9fdf9616b5f51a65248fa3e39",
        "abilene:diesel_units_authorized": "e79571a75660d557fc00e137283198c878fe1c9c5eef3de96291e90fc9909838",
        "abilene:diesel_units_installed": "9005240c964d577e7936e98b83071d3cfb41c25b110ee8bd96fb01d8de600d48",
        "abilene:early_training_inference_live_by": "125499447cecf5bfd0afd24eb4326470b4ef3b52dc0f9cb5d2cd33dc53ca8fad",
        "abilene:exact_workload_start_date": "64e7c510b01aaca15b29bd76b1aaf4548587e0d10046017c6d94345714752b2f",
        "abilene:gas_commissioned_mw": "fcf1ee8323e261062fbe835d823bd8348b402290b81d37376c3744693abc40a5",
        "abilene:gas_permitted_nameplate_mw": "7df3dd6e3fcd2bbba31b7013e6199666be9ab329d612eb54537488b92beacd57",
        "abilene:gas_turbine_units_authorized": "ee9d3e4a9be67d84cdcab0f608d65a6cdc1a277d3db75642b9fcd667c8c1eb63",
        "abilene:generator_terminal_model_voltage_range_kv": "55066ce1c186febaa396f4aa323ae7df99f73e0890ba32c56466b9702f4592b0",
        "abilene:generator_terminal_site_voltage_kv": "10433bce6b3f91cd8c514281b3d571a73245aa86c46d616ae805333fdc48cf3a",
        "abilene:gpu_design_ceiling_per_building": "7f0c3c4fa2dc437b61f2f2237e1df338d98e2969286781aafa190ee80e8c582a",
        "abilene:grid_expansion_fully_energized_by": "d360b8fe51d5fae24fd9d001cda50dd2c0307e25337026e6adcbe89362bacc62",
        "abilene:grid_expansion_substation_capacity_mw": "65f69531279b2f09133ccb3a5cb14db8e28fdc45fd935ac1c38e62d0c606bb50",
        "abilene:grid_expansion_substation_voltage_kv": "29fcf2612bfbe82e6b9664559d61a37d1e580678bba07c3292308b93f43bd2e4",
        "abilene:grid_expansion_transformers_energized_count": "646342349bdef286dbc08fcd5c7f5fd2f51c109759f9e350599968fb42d2ec65",
        "abilene:grid_expansion_upstream_line": "85869356b832b60a825ad9b17a6ec3711a525a2c141bab2ef80a259e5d0d8492",
        "abilene:grid_initial_service_operational_as_of": "ce3db0d6045e858ef5804dc2bebe99e6f1b360a3e9fc10de8cc51d4efdce8da3",
        "abilene:grid_initial_slack_span_length_ft": "d68d096eab3bd31dca75bf38b162bcc12f4041b80623684b2e762c0b79e67ab6",
        "abilene:grid_initial_source_line": "b4a98c1fca99c41de9fdfa8963d99ac7f856da0e10411ff10be0772bc8f19e8c",
        "abilene:grid_initial_substation_capacity_mw": "7b73be2c3b1ba830f2e1a4b4934da1f2c0988fdbbfcf0574a105ffd3e6389662",
        "abilene:grid_initial_substation_voltage_kv": "f91b83d1182e025b5f8718b306e9954be052afd122e37e290ea2d85926c2d8ee",
        "abilene:installed_gpu_count": "b0da66732edaf89c13cdb75ba97ce269af57c7bfe435f04929e347b5e439a391",
        "abilene:operational_buildings_exact": "eef97192f9e21df32c186561fcb81b82f3b40c6ab16717e702ab857d8e7a5657",
        "abilene:oracle_capacity_delivered_percent_untyped": "4be80d497612c58a40127a62fdf02703de2827eb3e7ec67e91483da3d848022d",
        "abilene:planned_grid_interconnection_mw": "5eebb58d7d26c7af3e496f6adab19bcad05f031cf8fc805af664c462ddfffc79",
        "abilene:rack_air_cooled_components": "94b699af9d8440c53ece2aa263544272c8b9cb8b4c893cf1c048df1b91b161ad",
        "abilene:rack_liquid_cooled_components": "269c899d6eacd89fbb8cafc17feeb7c1cfb8f6267e954e2eff17a957f618174e",
        "abilene:rack_platform": "dc4d06fac4f2634cf0df6762329bc24eba6abbbdab16209718a2c9c96af60578",
        "abilene:rack_platform_nvl72_design_reference": "1f0bea72e46f3f83c9a25eede5b8ebe65ea2ec7c8dca9629f75ed138cb5f75d8",
        "abilene:rack_power_shelf_ac_input_voltage_v": "8d038f02143bf0b8585019ef8829733781d2ee1c2bfe5107378e15c3822f775c",
        "abilene:rack_power_shelf_output_vdc": "302c60e938ad78de44081e8f0389b3adc8b68570bf6bde2b4796e49c058efe99",
        "abilene_execution:building_electrical_delivery_scope": "56144c2d9d334c5c10347fafa8b41ed0089419a75a8d1759833d1e526fb2ce7c",
        "abilene_execution:building_power_train_as_built_configuration": "5114acbd84b15cdbc508af0efc1593a2b612c9dd4534ae8f08e198914386cace",
        "abilene_execution:campus_construction_start_month": "aec957a863f830eb7f7d78b635d8b8bfc48feef7a93ec95f34a72a43c1e6837b",
        "abilene_execution:cdu_site_configuration": "fa6f94d9012901b9242d0da8846569812be06f1bec6370dfeef521494d680dac",
        "abilene_execution:contracted_grid_service_capacity_mw": "9cef2375e95758e2e5f84b5b14761fdb93dd4e008e29256be28dcec12e731620",
        "abilene_execution:current_critical_it_load_mw": "4d02dcacc0a4ba14570d2ec80fffd68e7ca16a9fd659d0172250ab11ccad0e21",
        "abilene_execution:current_operational_building_count_exact": "005a2bc17e54f7a55e7bc5a0878b0fc5280bba0e10f9f1ef0f0f522b1b7ca7d2",
        "abilene_execution:current_total_facility_load_mw": "31e38bf668ebb4aa482b75c30a07a2ec7e45226708b01d1c02adddc4c6b311fc",
        "abilene_execution:early_training_and_inference_live_by": "b4f9973a02c5ac26116c6721ed68e522c9374c9c80fdc805c8ebe49e44b78e6e",
        "abilene_execution:expansion_345_line_finish_date_as_reported": "4d876f3bb002da69a62759a76d16838b6796c3c3c516d0f09df6caaa6978945b",
        "abilene_execution:expansion_345_line_start_date_as_reported": "94f62fe59b709bedc816928a1419b1632ea7cb9d40d3ee8867fc535ffad99c95",
        "abilene_execution:expansion_345_named_line_project": "baa57f47eff87e84810e11fbe915eafa795015579bdf466e148a9844ce210f61",
        "abilene_execution:expansion_permanent_transformer_swaps_expected_by": "7362d8664403f20c475f7963eedb21c5ea8840fd5e4e5c83331614c5712eeb8f",
        "abilene_execution:expansion_substation_all_five_transformers_energized_date": "cdd47534872ecc5327348de4c4d81ceb88299a5d4aef023a358f70b73b71aaad",
        "abilene_execution:expansion_substation_first_transformer_energized_date": "852e9a14d2122ac5010d9aad3b9e85060137ffc668611d6871c23e35fcb1e282",
        "abilene_execution:facility_cooling_interfaces_as_built": "ce2c721de062ff8b6b93425aa374761d334f9179c9849ef06710e767f4674c5d",
        "abilene_execution:facility_cooling_operating_measurements": "c374ed79c9caa347937e07646c1015ea35c5176ef59f3bb0af5364f4fe25ccd9",
        "abilene_execution:facility_cooling_pipe_materials": "c669db767586a2ed40fc99ea4dd1b7d488b268fc2a0025bcb61ecec9acd16e37",
        "abilene_execution:facility_cooling_water_system_design": "cd8b8374581c6a00fbc7f4daf37a31eabb5e8b70dfaf81e30029f25ef396d008",
        "abilene_execution:facility_heat_rejection_terminal": "4ba3130086096967cc3d88b9c3efcb1d5edc9626af888339274526d587d019e1",
        "abilene_execution:first_phase_operational_by": "7be6646e738393ddd46ff1539410d7c50551b3d5b586527840d0ba5cbc17b995",
        "abilene_execution:first_two_buildings_energized_by": "51e4fcdd4b83f5af02ab35c1aa5a9adfd8987de4fdedd5d49930c9a2d23e459b",
        "abilene_execution:gas_turbine_commissioned_capacity_mw": "7c708aebfeed5b2aab4abca0a48fec0b31d9a6922e7ad8b5f14c2e8ec2506a78",
        "abilene_execution:gas_turbine_current_operating_posture": "9ebb3fd9e4161d9263ec5a505a3360be1f6eacab13de0f439c45efa52ff740e9",
        "abilene_execution:gas_turbine_current_output_mw": "4612740e229f105c08b05836f807007b5717dd654b65d4fc8566cbe07d7c88ba",
        "abilene_execution:gb200_first_rack_delivery_month": "eaf624244e57e02652529d9a921d879435a49510c0ec10a799beb6b0277606b0",
        "abilene_execution:ge_vernovas_gas_turbines_installed": "ae8daacb3249abd7517199bab6f91a7dad3b1d1c000b9969538db458aa298b2e",
        "abilene_execution:generator_gsu_protection_as_built": "8f09d0006515149d829f227ecf0973412930d29624a76d7ba1caeea29380a147",
        "abilene_execution:generator_terminal_site_voltage_kv": "47d6ebbdf7617b15ef99351771f04d96b6bbf049358200b784372df4c5477556",
        "abilene_execution:gsu_as_built_ratio_and_connection": "a7ba144b9854be417185238fb9a05e82f139760170afa210172c743bca326af2",
        "abilene_execution:initial_aep_poi_energized_date": "b8a8fe074f4024ec2569fc8204a620849207141503afc2dc79fadb798e903e31",
        "abilene_execution:initial_aep_poi_scope": "df7ab1638ab455f3fe4796638db57958fd5176b8f4907681ad8134b31ff805a9",
        "abilene_execution:initial_aep_terminal_energized_date": "4965e45b9d9380acadc0bbf97351cf222735d199f34420fdb79803600fbce6d0",
        "abilene_execution:initial_aep_terminal_equipment_scope": "f6020ef00e004bd49a5adab4f5f00e02adc9b23f270dce9443ad4558b239b513",
        "abilene_execution:installed_gas_turbine_intended_role": "fdff5465f8da6fe658b8b794c954499f167a88181324e1d4bf9ae419ae36805a",
        "abilene_execution:installed_gas_turbine_model_mix": "22f85c2e5f1b6b7e281979ae1697a459ab275e9d105b58d14b87cf4afed1f9a4",
        "abilene_execution:installed_gas_turbine_unit_count": "b8ea73c059833b62d3c5304a67ce1de6ecd4c51eb89a5ddba0898ec04c23ef80",
        "abilene_execution:onsite_power_plant_delivery_confirmed": "48fbd5e61cd681768252f568743c4f78c64401c21e199d8b1476685432d1eb03",
        "abilene_execution:operating_rack_configuration": "3191f571d3e8ca929096a66b9542ab25139dc085f448ae193e604855775c6970",
        "abilene_execution:original_remaining_six_buildings_planned_completion": "c3956d774bb68775fc6372cbc0da6baffa074ad80893a4302ece83b901af3319",
        "abilene_execution:rack_site_core_voltage": "5e99a42b52a470cbab14d46e8167e12b1c077930514f031edf905999330bb417",
        "abilene_execution:residual_air_site_configuration": "2003d8308f0eef32fc4ae29003605ded44df849cfae7ca625a718f5efcb42451",
        "abilene_execution:site_specific_interconnection_queue_and_contract_record": "f0c1c7196d4c189893bffffda679f28160fa13edadaa06e7073f1fa86b0d8000",
        "commercial_compute:abilene_2024_crusoe_owner_developer_announcement": "0c94115b7a9dfc28bd18efe071f588e44571686cff3f285b3f6dfb96e4f2e72b",
        "commercial_compute:abilene_accelerator_active_utilization": "ab9872762446e933cd41a7899262665e1c29b1dfbe8d9b8019742f0af95b018f",
        "commercial_compute:abilene_accelerator_power_share": "dc1021c1956540bb9eebb8acf604103c3b30fb857e47e94d8f2336aa9f48a0d1",
        "commercial_compute:abilene_capital_stack_waterfall": "259ad1c44d337ab1ea4fb7f838e119333e477597a091e6c70b97524ef290c784",
        "commercial_compute:abilene_compute_activity_roles": "9b7bada765a237deb081aa2837947a5281f49fabc69c096dcb12d6c7729d21e2",
        "commercial_compute:abilene_current_facility_power_mw": "aba0be54404734f903f3ab5d930544fe20cc66225c28bd6b1dd45bc618982913",
        "commercial_compute:abilene_current_it_power_mw": "7a8f95501423a62c0e0fca4342ad48f3ccdc86d939020cae9ecb51cdd3740132",
        "commercial_compute:abilene_current_pue": "279d951b459e5d43312cac3921e281010a88fc2e051fdd0cd1bd5f1a4111a4af",
        "commercial_compute:abilene_inference_batching_configuration": "5bae697f26f9327d5fd2dfef7a23ed6b3d244855b8ae1a7912f1a780b36a30a9",
        "commercial_compute:abilene_installed_accelerator_count": "7dd5bf1b9f52f7e9dd10598c4320897884c54ae4c5717825767b3749ac157230",
        "commercial_compute:abilene_it_equipment_financing_terms": "93f4a1f3bfd3a8443d11e0d60733a9c722a35d5294048234c3e4420eaaf72b80",
        "commercial_compute:abilene_it_equipment_legal_owner": "8b2641c106deea9ba342d52181c189c9a05be7d21301690636b5d6b6c4e6ccdb",
        "commercial_compute:abilene_lancium_development_role": "bc964e8fc49e0b8284fe69c9026405beee317d615dd4f2f5df28bf7a04470f0f",
        "commercial_compute:abilene_land_legal_owner": "5b053eb93e92ac783a7ab6461473e8bacfc9a5d7addf54e231418d1482d62bd2",
        "commercial_compute:abilene_measured_token_throughput": "a9a5c60699f0bd606eee84de54b140d1859778c46655a4c5210c1f0a555b4da5",
        "commercial_compute:abilene_model_and_workload_configuration": "91682e10ebdbf152b37a33447cee4ac681279d6c1a36f009ee149598411bd609",
        "commercial_compute:abilene_phase1_crusoe_delivery_and_operations_role": "63ac14fbb22086220e9806db1bdba02b19763ffcb37741229aa2c53ed43fb885",
        "commercial_compute:abilene_phase1_financing_structure": "49417a1dd6ae8cde94569be39bac70b0061c9b34a36c9aef5f3ce8e28e75f53e",
        "commercial_compute:abilene_phase1_lease_structure": "c8ad533f23f82802e1b60b550c34bb35bd740a42b0df316bbb026939afe54b95",
        "commercial_compute:abilene_phase1_lease_term_years": "493b8505f3e83338d8a7b90352385fdf4e66b87b3e1db2dd2e1138475860d3c7",
        "commercial_compute:abilene_phase1_tenant_identity": "575277440ba0cfa4eaed41205e3faaf1213146eff7af358c1027769dd22e5bc3",
        "commercial_compute:abilene_phase2_financing_structure": "c2157b97f73bf23da7b21f9e552c6b2adef29b69c46b91fc7a51f2b5ef6e729c",
        "commercial_compute:abilene_power_asset_ownership_by_component": "5fd72f50fa132d33152bd96bb154db3f9e5da50aab653d00d7fe5d1fd1adce98",
        "commercial_compute:abilene_rent_commencement_and_acceptance_terms": "265f3084a7fe33cf4a899e023b3fd704ae76172c081e406823e304dd01457cab",
        "commercial_compute:abilene_training_mfu": "6e7a240f0722f2733862caea19dac6011ae2465ecc24cc33ff8d800297b31754",
        "commercial_compute:abilene_usable_accelerator_power_mw": "20c45a2913e7933fcec3b4e5abfbecf32d01b71fefb5c00708122f681717d544",
        "commercial_compute:abilene_utilization_risk_allocation": "908d7440aceaa00cf7a26cc9801e66707c481e4c5bb4e7b5959f841a96d0c1e4",
        "commercial_compute:coreweave_ai_cloud_contract_and_financing_comparison": "b344ae396dda730c47d4855b5fb1b2e2bf89e8f88943e99f6de76313e6159fb0",
        "commercial_compute:coreweave_capacity_and_utilization_risk_comparison": "26eba0ea8893b9dee7c0fb4ba394865d129d3fa31c5223531364a8c47be570fc",
        "commercial_compute:coreweave_facility_and_equipment_boundary_comparison": "ca73291e0ba42717b9fb2860041385dd93ce24e844322fc8da4c6957b1b4b044",
        "commercial_compute:dense_decoder_training_flops_per_token_method": "0110ea3d68af528187afbcce5459b980bf031bf76ad3132b1a8116f1ba032f55",
        "commercial_compute:dense_decoder_training_tokens_recipe": "cbf678d5cf3be6ffe48cb70563819b92cc3f4c1ba7ce0520ddc64c018604d2a9",
        "commercial_compute:dgx_gb_nvl72_product_reference": "48047a1898c6e955473e0a0bc9bb2c0cdebcdf66ad52d3843c69656747c014fe",
        "commercial_compute:equinix_asset_and_operating_boundary": "4540a40b837634946c4531fca41fe293b02fe470d62b8f8a4c3820c6a04b1137",
        "commercial_compute:equinix_colocation_comparison": "40f9469c842efb68eb0c3a3b9dd4c0ad803614f8637e3efc5cb22f05c0dbce1f",
        "commercial_compute:facility_energy_to_it_energy_recipe": "bf3b8f828cffe740e56625fc84defa0fd8705030c4e292d5047bc989e77765da",
        "commercial_compute:inference_batching_dependency": "ea8cfa31900d25e84bbf26f65c32cbb5389d482c027131078d4928373937502c",
        "commercial_compute:inference_measurement_boundary": "4ccbc7a91be806d7fb2c86fa82daf425c1df009d37d767512f6349ffa3402403",
        "commercial_compute:inference_tokens_recipe": "6449c62058a1bfd43e2c67a34bae6585c66b0f733399e82f971340e61f4b3da7",
        "commercial_compute:microsoft_hyperscale_cloud_comparison": "5afb12af6796467bcd38f48847bdc13fcea0e5df795ee393bbfeed0aeee9499a",
        "commercial_compute:mw_to_tokens_scenario_recipe": "896dd883046bc785719a9ac8f9580bf00af26a29f13684831d4ed0ce06ddc936",
        "commercial_compute:pue_energy_boundary": "277a51f80cf6ac969d9a9c334c5a8edf55580dff01a8141d1933889e9382077f",
        "commercial_compute:stargate_initial_equity_funders": "91b6a2b6363686e68eb465161b7333a07d8bf8c9809383aca7be0055dfecd77d",
        "commercial_compute:stargate_lead_responsibility_split": "a1478cb3ed82e7972738e8644384db85d508008d65477b56240e11425a15c2be",
        "commercial_compute:training_mfu_definition": "79c1937b7d0357470169d1f64685b6b5b3d28fc53095a18f6bdf613877c4d6a4",
        "commercial_energy:crane_microsoft_ppa_contract": "6de9f5752e19422deb35b218ab5114b149c6b99e032f63d3de3d3a86dc65c191",
        "commercial_energy:scope2_contractual_attributes_not_physical_flow": "7a931e8b82eb0a8131b2378b5811341e1fae5baf39dee7cb435307bcd40c82d0",
        "delivery_resilience:abilene_bess_function_rating_connection_operation": "0bdcf7cf6bc29b489588683df6d58da50d4ea2e3a626f7e331b2851eab1427f7",
        "delivery_resilience:abilene_bess_reference_design_status": "a30648be87d92f2f23c9c8286b44ff1d6db348d774c1b103b3951f07866cfbad",
        "delivery_resilience:abilene_operating_transient_profile": "3b031b368809125051828b91d4e91fe064b9e6aab4ab5d3390470e0bda0f7512",
        "delivery_resilience:ai_training_checkpoint_transition_duration": "419ac9f3066b4ec625d6a31ea9f681ad97cf4ec1e6aa55edb4cd144d13fc51c7",
        "delivery_resilience:ai_training_observed_ramp_rate": "8e8491430acbacd689134b9724f18c35f4c1023f2fbdac22dc8fd85b15cf7dd4",
        "delivery_resilience:gas_turbine_slot_can_precede_site_readiness": "6307b6b5fa2a52889db92b6d7a3117e3f7ca76a1c1cb63c0c4823d0081a0b01b",
        "delivery_resilience:ge_gas_turbine_delivery_slot_exposure_2025": "15408da8caae5bf8bea306b3556ba29895c311d8bd21b8315f136651bd00cb5a",
        "delivery_resilience:google_compiler_power_shaping_result": "8f1e3399f013ddc0783d784b0e359badadf79f8d5654ea74253da62c45a1064e",
        "delivery_resilience:google_synchronized_ml_fluctuation_observation": "e4e24e86b64007465f371772db30392a43b568de40b50ab9da5f0aed245f8e29",
        "delivery_resilience:large_load_grid_response_mismatch": "1ff976e26bc91013c75d912ee19e2e64d0942519ffe7127202eb7712f9dc376d",
        "delivery_resilience:large_power_transformer_delivery_chain": "486d2d2b648bb5fca9f78b551acc22ca26bd51a151649e56b7e668a6a8f7ed6a",
        "delivery_resilience:liquid_cooling_acceptance_sequence": "d45adad6b1a9a0c649ad1f61713d1b8e50bd94f5c271649dc2b817b6a990308e",
        "delivery_resilience:parallel_ai_load_correlation": "f1489c0bc4afa296e4b2058c48919f9eca24ca530c8719a7ff658de2486b34dd",
        "delivery_resilience:standardized_row_cooling_lead_time_2026": "d75aa17376ae1129d87088bae126509fb98e80ab52019c0c6bce963578a9b43a",
        "delivery_resilience:uniflair_xca_initial_shipping_date": "781981654c402a46ae6fe03907119480070cacaa4309e44cef64d975c92609bc",
        "delivery_resilience:ups_and_btm_bess_role_separation": "889e1f8bc1a8bc1b195ef9f813665a189e14816facb1e4927fe2c7e9b8e9ef22",
        "delivery_resilience:ups_ridethrough_depends_on_site_settings": "1252493b703c4c927389165fd42307f3502c1cd7630eaf813cc7618051243d4c",
        "delivery_resilience:ups_short_duration_ride_through_role": "ee16190d4476eeec3ecbad1c48d01739a09fba4c0278d6725c79af9b48c9a684",
        "delivery_resilience:us_distribution_transformer_lead_time_2023": "04623a6a1d63e5e468fd856b4ee9883133acf2d47efd3fc034f6887bc4f06a4f",
        "delivery_resilience:us_large_power_transformer_lead_time_2024": "2ef87795499e79ba18595c788e8a555bedc462fc752a56a7955ba398e5975f15",
        "delivery_resilience:voltage_sag_data_center_load_loss_event": "18b9029b340b51daca41e508140e11a426a42b976390f0b0e220e0acb6312bb5",
        "electrical_engineering:busway_feeder_and_plugin_distribution_role": "e2cd2cbef26dc091a877b59dcfbc48fa182f62983c15892d8c555d2bafa62145",
        "electrical_engineering:generator_protection_fault_scope": "c4a31b0fd2c67b7b83285ef574157b7f0f6a4148bbbca1ae91b3ae8fdcab2ea0",
        "electrical_engineering:generator_rotor_to_electricity_conversion": "6d78a0a129068e43029bc220d2c7e698c690b7d9bbedf7f864727948a2f5a2f0",
        "electrical_engineering:gsu_generator_to_network_voltage_function": "46c18c892fda47fbdb44e267e778610db4aead27407cbdc99404852c4bb5e03b",
        "electrical_engineering:gsu_protection_zone_application_specificity": "310e4c258341f7cc6863829532d746e6e8bc3bf0ecd7e221fa999ce3e7f7400b",
        "electrical_engineering:low_voltage_switchgear_distribution_protection_role": "56b4f78312c5b40944a034ee226b216df7a5a7b5f4034ae5bb91dd24b9cc325d",
        "electrical_engineering:multiphase_processor_core_power_role": "e0d1b418186a7b258359f005362900f2f7ad6030678bad56a822435c60b57ea8",
        "electrical_engineering:transformer_protection_engineering_scope": "5765aefb95f45e50ffa3c75a94395e3a6054b9472a2c2ea819330e28c61e0342",
        "electrical_engineering:turbine_fluid_to_rotor_conversion": "90c34076ebf909afca0d60b3a093bbd3e8a073d9651f1199890aa3c85a6db5d4",
        "electrical_engineering:unit_substation_coordinated_assembly_role": "221269682725007a7c23495b9d280c47d40ac738f128c35f1990908f4503fe08",
        "electrical_engineering:ups_conditioned_no_break_power_role": "8a755a0dd7ab606dfb9b34afc0cd9608d83b0bf749d1d9000f02b7b78c0666db",
        "electrical_engineering:vrm_intermediate_bus_to_xpu_voltage_role": "2127ed8afbcdc5031d632b60f2a814153199338e121a71b6f6c49bd726de3b03",
        "electrical_engineering:xpu_low_voltage_high_current_requirement": "48e5f50a9ba3c3054dda5b42b891e4cbdb2e5a6a14b66c18ea9aff040ae40e70",
        "thermal_engineering:generic_cdu_control_functions": "d054f6c98dbc42f8de5a3cbbce45a07df7162ee943e5c274e708cef1a3a94a1d",
        "thermal_engineering:generic_cdu_loop_isolation_heat_exchange": "9ee913d4e94cfc9a844af55ac7fcfb39c7d0daff64454fb4cc9592fc3034dc7c",
        "thermal_engineering:generic_cold_plate_heat_transfer": "2d4a4a57d103c59aceda88a4e1c7ca26e65c579d0668100365865ebbbe9345c5",
        "thermal_engineering:generic_crah_air_heat_removal_path": "111fa6fa62b5c9526fc1b787f862f72dd76655d9ec0a46a6708a2d1f3894239b",
        "thermal_engineering:generic_crah_variable_airflow_control": "1c4c75fd800aa0109fbeaf5c125927f91420e537c263b30dc5719500763e5ac8",
        "thermal_engineering:generic_facility_loop_heat_transport": "9b09cd51b8950df28b607c478973240f5310d5a90e9dbd214f087d310c8aaa77",
        "thermal_engineering:generic_facility_loop_load_control": "7d050ac239c70ad6fff10f1adfedc25b49b199d8d8f1e2734004b95b727fcaae",
        "thermal_engineering:generic_ite_electrical_input_heat": "2696dff6eaca90314ca8175b85291fd35c112f61a525007cad48914e326f672c",
        "thermal_engineering:generic_parallel_liquid_air_cooling": "9d5adbf02c07e2ce6ca6929cb569ccebd59b67fc941e060db3d8081b1ac794f8",
        "thermal_engineering:generic_rack_manifold_flow_role": "2d644f6da2216fa9a88c0b6412354427ffcc74bf7f4e2fa0e6c5877265940ddb",
        "thermal_engineering:generic_tcs_supply_return_path": "a3842b2fc5f5852607c7cd9023db61a8994e0d016e53f1d50c4d85f9bb52e9a7",
    }
)
COURSE_META_FIELDS = {
    "course_id",
    "inventory_scope",
    "status",
    "runtime_minutes",
    "relative_weight_total",
    "master",
    "cameras",
    "evidence_ledgers",
    "master_evidence_ledger",
    "sequence_rule",
}
ACT_FIELDS = {"id", "title", "learning_objective", "evidence_ledgers", "segments"}
SEGMENT_FIELDS = {
    "id",
    "title",
    "opening_question",
    "learning_objective",
    "weight",
    "depends_on",
    "camera",
    "node_ids",
    "edge_ids",
    "evidence",
    "transition",
}
SEGMENT_CAMERA_FIELDS = {
    "anchor",
    "shot",
    "mode",
    "status",
    "reveal_ids",
    "reveal_copy_ids",
}
SEGMENT_EVIDENCE_FIELDS = {
    "readiness",
    "claims",
    "promotion_guards",
    "blocking_research",
}
SEGMENT_CLAIM_FIELDS = {"id", "assertion", "binding", "fact_refs"}
COURSE_CLAIM_CONTRACT = MappingProxyType(
    {
        (
            "p0_gigawatt_not_workload",
            "planned_grid_boundary",
        ): "75dbde2e0ca56ccceee4f3e333bb6ff031a68f92b589c55e29abca3c15ffc9c8",
        (
            "p0_gigawatt_not_workload",
            "initial_substation_rating",
        ): "7deefb81d1467a7c32cd8a5309ed27f8bfa49bdb9e6710ddb3b9f3761ae3f843",
        (
            "p0_gigawatt_not_workload",
            "expansion_substation_rating",
        ): "5976255492d5a51b154b0357834c4e885b7e0271274f73529c60e16bbfd12cb6",
        (
            "p0_gigawatt_not_workload",
            "permitted_gas_layer",
        ): "59fceb1fdec58b90403933b853fdb357f3d6c1c51cff0c299276cad64da7c490",
        (
            "p0_gigawatt_not_workload",
            "permitted_diesel_layer",
        ): "f5758a9c6d872199257dd19ac96cd03be427857b9cf741c0af8a86efd3311079",
        (
            "p0_gigawatt_not_workload",
            "energized_building_minimum",
        ): "7f8df0527e34996c09778adc2e759beac2a49e5eb4025b3505be9a22ac3bf8c8",
        (
            "p0_gigawatt_not_workload",
            "operational_buildings_unknown",
        ): "8890c6191981da2ed4e712454683f355bea9ac73273863c511444a6e61f047e1",
        (
            "p0_gigawatt_not_workload",
            "installed_gpu_no_estimate",
        ): "7aae6e8d52f729005dda8736fee34ef0ca74ecb25e986c7e9932d9f6b1e74a6b",
        (
            "p0_gigawatt_not_workload",
            "workloads_live_by",
        ): "c3f1666fb4a865a0ebfe2d3b6c0fc541d57d453a0d0699acdc5569da1cac1d4c",
        (
            "p0_gigawatt_not_workload",
            "untyped_delivery_percentage",
        ): "93890faa661992ee6107a565cef0937497b1f3b2a671d48a140e94e255af9580",
        (
            "p0_gigawatt_not_workload",
            "adjacent_project_exclusion",
        ): "d73d43a8129c44360ea7b3362a62b30b6ab6500a5041ded28cb9bc1b236a11cd",
        (
            "p1_read_the_machine",
            "energized_example",
        ): "1118950da9e6eba8c81e474165d11546fb36739460a9c3ab251e06bfa4b4299a",
        (
            "p1_read_the_machine",
            "permitted_example",
        ): "17ae550cf3221589c1c6792e15d095dc59ee288f9d071cec8035ec630a63ce69",
        (
            "p1_read_the_machine",
            "future_example",
        ): "5de256c19f9104c0808eb624ba8915b93d476ece4fb2909438593493d253753d",
        (
            "p1_read_the_machine",
            "unknown_example",
        ): "d5e18a9b4baeead1a0aa62ee4479c32867952a0e95bcdafc8f1e12a75c67b8a0",
        (
            "p1_read_the_machine",
            "selected_design_example",
        ): "c53802e6ec2f7484c67b444bbc83c43bdfae28f8fd8414f21039055e2ad18eb1",
        (
            "s01_fire_to_electricity",
            "gas_authorization",
        ): "9269b5e7b7ecb2bc0df3ad4a4909d637fd8d8cec4940641b0c0510d9b5c04946",
        (
            "s01_fire_to_electricity",
            "turbine_generator_conversion_reference",
        ): "76f164a0c7e2701e17ae5a3c50d82c02d70715f8d0f9efbea433f2e6c5c9132b",
        (
            "s01_fire_to_electricity",
            "installed_turbine_presence",
        ): "5cac7db825e48d48bd2b537477e1bd664eba72252aa44e7b272f4a48c0916b00",
        (
            "s01_fire_to_electricity",
            "installed_turbine_configuration_unknown",
        ): "b96035267b8eb3f046c6489d144738d8a2900dfd44f1d09a6eb9eb2aa6d2b491",
        (
            "s01_fire_to_electricity",
            "operating_posture_unknown",
        ): "b122979ec43dec6e55a950387367755d71314075491cbf520318fabd4e8002d2",
        (
            "s02_generator_terminal",
            "generator_authorization",
        ): "17ae550cf3221589c1c6792e15d095dc59ee288f9d071cec8035ec630a63ce69",
        (
            "s02_generator_terminal",
            "model_voltage_range",
        ): "16e3eaaea41b119b70f8e2a3386074c9028c56b5dadfe2a36f1ebd443e3046cd",
        (
            "s02_generator_terminal",
            "site_voltage_unknown",
        ): "132d59ae27585b87fb29c04ec7339294433dc68f7efe3eef8ac40ad26146ca4c",
        (
            "s02_generator_terminal",
            "campus_interface_design",
        ): "9a5a026848ba278f2b3e64999dda1657d2f74c797219fc37161805b774dedef7",
        (
            "s02_generator_terminal",
            "campus_interface_unknown",
        ): "d5e18a9b4baeead1a0aa62ee4479c32867952a0e95bcdafc8f1e12a75c67b8a0",
        (
            "s02_generator_terminal",
            "gsu_function_reference",
        ): "4d89a54e8cb2dfe61917a1510a3991759d15a979e1d04a14fde8881eb76373cf",
        (
            "s02_generator_terminal",
            "generator_gsu_protection_reference",
        ): "383bd7e7f411625da26b538a6530d41c27e33b29f2dc6db643cbfdaa96dc98b1",
        (
            "s02_generator_terminal",
            "site_generator_configuration_boundary",
        ): "124c6e34b0b1aaf6a1ba588966aeaf137c91be0da236cf640cf4fac0dadf09c4",
        (
            "s03_initial_grid_path",
            "initial_service",
        ): "f7317de57a1b4bb7e4559ba46a58277ac90b775d115c6611fa54d1d250efe908",
        (
            "s03_initial_grid_path",
            "downstream_merge_unknown",
        ): "eb2ee74f372e7dbb17a38b9155606e47867b943ee0ba9f3fe64a95a0aeb3505c",
        (
            "s04_expansion_grid_path",
            "expansion_service",
        ): "c62d229120792730323d57601893e074fe3efa0961062110c686486cf98c3f7c",
        (
            "s04_expansion_grid_path",
            "upstream_source_unknown",
        ): "69ded4f93224c1446cb525caa69213b0f58be89325a8d6a60ffbcd1f39fb49e5",
        (
            "s04_expansion_grid_path",
            "downstream_merge_unknown",
        ): "eb2ee74f372e7dbb17a38b9155606e47867b943ee0ba9f3fe64a95a0aeb3505c",
        (
            "s05_ppa_not_wire",
            "crane_microsoft_named_ppa",
        ): "93a4999097054997a62a151a3401c7ab0749aac05a65b0de375d243f81cbc1e4",
        (
            "s05_ppa_not_wire",
            "contractual_attributes_are_not_physical_flow",
        ): "b485e312992ff4cfbf4a63e24d2623647f41bbc18bcfeea5199bbddba2ff8a6b",
        (
            "s06_campus_mv_envelope",
            "campus_design_reference",
        ): "9a5a026848ba278f2b3e64999dda1657d2f74c797219fc37161805b774dedef7",
        (
            "s06_campus_mv_envelope",
            "campus_as_built_unknown",
        ): "d5e18a9b4baeead1a0aa62ee4479c32867952a0e95bcdafc8f1e12a75c67b8a0",
        (
            "s06_campus_mv_envelope",
            "source_merge_unknown",
        ): "eb2ee74f372e7dbb17a38b9155606e47867b943ee0ba9f3fe64a95a0aeb3505c",
        (
            "s06_campus_mv_envelope",
            "bess_future",
        ): "5de256c19f9104c0808eb624ba8915b93d476ece4fb2909438593493d253753d",
        (
            "s06_campus_mv_envelope",
            "bess_operation_unknown",
        ): "f1161459a3cc8ef541a4c6c80cc3ab4f5bb8e2a236564a84b4c6039bb2d340ce",
        (
            "s06_campus_mv_envelope",
            "bess_connection_unknown",
        ): "302b548e7f896e7ed1e21ea5b48f674a66d3f9b1bb80f54246ef8f866f37ef1c",
        (
            "s06_campus_mv_envelope",
            "diesel_authorization",
        ): "36150cdbff35a493137a8d9dcc9108839349329c8e1625da4a7be9ac7144f913",
        (
            "s06_campus_mv_envelope",
            "diesel_operation_unknown",
        ): "c15051811f2eebef01e9dec17f60a580ca09905bc2e5485442fe0767b27424b2",
        (
            "s06_campus_mv_envelope",
            "diesel_connection_unknown",
        ): "807a4f6faf8dbed1b0b9300acad91b9b9efe83ba47e6732212edafe52c292c17",
        (
            "s07_building_power_train",
            "campus_input_unknown",
        ): "d5e18a9b4baeead1a0aa62ee4479c32867952a0e95bcdafc8f1e12a75c67b8a0",
        (
            "s07_building_power_train",
            "facility_distribution_product_reference",
        ): "a71d1abd6dce596a6ec2adf9d7167a081a302b80e1c9ee26b12414d845ad3324",
        (
            "s07_building_power_train",
            "ups_function_reference",
        ): "bebef4441ca2f39e4df00874afe4960b520cf269a3d861b87450bbb9b0b5c30d",
        (
            "s07_building_power_train",
            "first_phase_electrical_delivery",
        ): "8b54d54cd72549a7cc28dd94a7b0dc5e93097c31363b11e3faa89033d8e52191",
        (
            "s07_building_power_train",
            "building_power_train_configuration_unknown",
        ): "abe8265ecb95bc400714b0fe66aeda191fb22cb10f437e67a61ac2eed84c722a",
        (
            "s08_rack_voltage_descent",
            "operating_family",
        ): "300de23c3a7ef43cfaf8634668860155a90d15a6732329fca2c4063c1696943b",
        (
            "s08_rack_voltage_descent",
            "design_platform",
        ): "143eb43b66ec95a4a2fd2df9e51c4a7c0843084b82dca62b9c5af04a49a777db",
        (
            "s08_rack_voltage_descent",
            "rack_dc_product_reference",
        ): "a4832442a3a67866490cf1eef43c3b98019a12c082305f55b9d83118744cac2f",
        (
            "s08_rack_voltage_descent",
            "rack_ac_unknown",
        ): "7c804ce41815cb80150636faf5af04b17f4c2bcd8023a2f97153b95628519365",
        (
            "s08_rack_voltage_descent",
            "vrm_power_delivery_reference",
        ): "6122bde2a4e5fefeb703dfb9a4f1723ce23b237109f013ba4a342b4a9a87428a",
        (
            "s08_rack_voltage_descent",
            "first_rack_delivery",
        ): "07633bce9360ea40bca6cee4dfe1b3a84dd0518caf0e43a5574680066746db74",
        (
            "s08_rack_voltage_descent",
            "operating_rack_configuration_unknown",
        ): "29ea8d97fa51a8bb74c8869effc79b63c9a4167576b6f913c46c53b3536f6dc2",
        (
            "s09_watt_becomes_heat",
            "operating_family",
        ): "300de23c3a7ef43cfaf8634668860155a90d15a6732329fca2c4063c1696943b",
        (
            "s09_watt_becomes_heat",
            "live_workload_boundary",
        ): "c3f1666fb4a865a0ebfe2d3b6c0fc541d57d453a0d0699acdc5569da1cac1d4c",
        (
            "s09_watt_becomes_heat",
            "direct_cooling_design",
        ): "7e383c7b28dd41abd0c284a24fa0d05c64a64b128edee055317e05c94f9e5483",
        (
            "s09_watt_becomes_heat",
            "liquid_path_product_reference",
        ): "53d692f20aca28fb43da503b90307250da7c4a3aa506d8d3eeca5fa2862e81b0",
        (
            "s09_watt_becomes_heat",
            "electrical_input_to_cold_plate_reference",
        ): "5457400a6b3b925c8a947c6e3646a5b75bcc5ab87d86e2a78c666a0ec00656ff",
        (
            "s10_two_rack_heat_paths",
            "rack_design_reference",
        ): "ad029dd29444ed882518d9d9b9f90918504c9f20b68ce9ba93beb4459a5a2f0e",
        (
            "s10_two_rack_heat_paths",
            "rack_component_split",
        ): "2e36cabaf27368e4f6661115e84fc6fdba06d8361a0e1c68650c22c20f8ee80e",
        (
            "s11_technology_loop",
            "direct_cooling_design",
        ): "7e383c7b28dd41abd0c284a24fa0d05c64a64b128edee055317e05c94f9e5483",
        (
            "s11_technology_loop",
            "manifold_product_reference",
        ): "53d692f20aca28fb43da503b90307250da7c4a3aa506d8d3eeca5fa2862e81b0",
        (
            "s11_technology_loop",
            "technology_loop_engineering_reference",
        ): "91f0d74bcab571e610a3e1c167869d977f27715c31070363c1e161d7b45ff0e8",
        (
            "s12_cdu_boundary",
            "selected_loop_design",
        ): "c53802e6ec2f7484c67b444bbc83c43bdfae28f8fd8414f21039055e2ad18eb1",
        (
            "s12_cdu_boundary",
            "direct_cooling_design",
        ): "7e383c7b28dd41abd0c284a24fa0d05c64a64b128edee055317e05c94f9e5483",
        (
            "s12_cdu_boundary",
            "cdu_boundary_engineering_reference",
        ): "2dcc72d67165ab73f50c8c6e9e5d5428b73a7c6d5941bdb8b4acb46f5cda7094",
        (
            "s12_cdu_boundary",
            "cdu_site_configuration_unknown",
        ): "5f849f3c40e4974ea8d06f49b09de15387e39376c3e6a7677da490cc7ec773ab",
        (
            "s13_residual_air_branch",
            "air_cooled_components",
        ): "545170cd3710ed71a9243b1ea600806227eac31cfa63d1d17bd53f033316d487",
        (
            "s13_residual_air_branch",
            "selected_facility_loop",
        ): "c53802e6ec2f7484c67b444bbc83c43bdfae28f8fd8414f21039055e2ad18eb1",
        (
            "s13_residual_air_branch",
            "parallel_air_path_engineering_reference",
        ): "0e594bb332f5155513c0180a99295d01cc77a8e1323f115029c95de3c6cfc54e",
        (
            "s13_residual_air_branch",
            "residual_air_site_configuration_unknown",
        ): "c0f99996fe2d0bcfce607c245c84d44f8b4e3792dc2a47bb4216b450b8b9ad43",
        (
            "s14_facility_heat_rejection",
            "selected_heat_rejection",
        ): "c53802e6ec2f7484c67b444bbc83c43bdfae28f8fd8414f21039055e2ad18eb1",
        (
            "s14_facility_heat_rejection",
            "direct_cooling_design",
        ): "7e383c7b28dd41abd0c284a24fa0d05c64a64b128edee055317e05c94f9e5483",
        (
            "s14_facility_heat_rejection",
            "facility_loop_engineering_reference",
        ): "af29ed6cc1c0c218a43bb1b1a0c08c27b1fca2262fac3a5e4187e89593583ef4",
        (
            "s14_facility_heat_rejection",
            "site_facility_cooling_design",
        ): "65914582e7fa8c42778588ab32bc53259c0f0a766d0939faf87e8bca546958cb",
        (
            "s14_facility_heat_rejection",
            "facility_cooling_interfaces_unknown",
        ): "8e4f711aca061a1b29add096e696a123eecd3f8d005b7c28a1b5dd8d100b5e0e",
        (
            "s15_water_accounting",
            "initial_fill_design",
        ): "192659ca9d43e3c9cf461890427695a6ad8ad6c223f2652461c2f8eefd01f2e6",
        (
            "s15_water_accounting",
            "anticipated_maintenance",
        ): "8847a8c90efb7d956f8082f622e03a924fd7a5ebc70c41be9e4a7a7264e8b863",
        (
            "s15_water_accounting",
            "measured_operating_consumption_unknown",
        ): "82b0b4cc77a0583a2ae2429018e680d38e1bb837441f8542be713404bf179cac",
        (
            "s16_close_atmosphere",
            "operating_family",
        ): "300de23c3a7ef43cfaf8634668860155a90d15a6732329fca2c4063c1696943b",
        (
            "s16_close_atmosphere",
            "cooling_design",
        ): "7e383c7b28dd41abd0c284a24fa0d05c64a64b128edee055317e05c94f9e5483",
        (
            "s16_close_atmosphere",
            "rack_component_paths",
        ): "2e36cabaf27368e4f6661115e84fc6fdba06d8361a0e1c68650c22c20f8ee80e",
        (
            "s16_close_atmosphere",
            "selected_heat_rejection",
        ): "c53802e6ec2f7484c67b444bbc83c43bdfae28f8fd8414f21039055e2ad18eb1",
        (
            "s16_close_atmosphere",
            "facility_interface_boundary",
        ): "b9d0203ad60815695dd81707d9e1db9094090b2bd4bdf5b37160ccb503050b9c",
        (
            "s17_interconnection_schedule",
            "planned_grid_boundary",
        ): "75dbde2e0ca56ccceee4f3e333bb6ff031a68f92b589c55e29abca3c15ffc9c8",
        (
            "s17_interconnection_schedule",
            "evidenced_service_milestones",
        ): "7a443dcf034c8194989624541c7d10dc151d2ec7df9a658d3f86ab7c8fb02086",
        (
            "s17_interconnection_schedule",
            "initial_aep_delivery_gates",
        ): "9f376eaf10b022273cd35a937f97794127754f15f515a240fbfef15b3d86c586",
        (
            "s17_interconnection_schedule",
            "expansion_line_schedule",
        ): "fc06fcb41e26475adad92c12381031234af2dbe84e3c1d1d87b3895ea762ba3f",
        (
            "s17_interconnection_schedule",
            "expansion_permanent_transformer_schedule",
        ): "382e7cfcf0d37dfdc8f80700fc37768016ec5a9d89bc9f9a182b5cc339dce148",
        (
            "s17_interconnection_schedule",
            "private_interconnection_and_load_boundary",
        ): "1197bb242b8c3e9f5a4b91bc37a13ae331a1e06b55e0cffac779c622dc632cee",
        (
            "s18_long_lead_equipment",
            "gas_authorization_anchor",
        ): "17ae550cf3221589c1c6792e15d095dc59ee288f9d071cec8035ec630a63ce69",
        (
            "s18_long_lead_equipment",
            "energized_transformer_anchor",
        ): "8aecfda77784441fac5f4b9fdf4b8963b0276688cbdc39b79c49e982f63e6c23",
        (
            "s18_long_lead_equipment",
            "cooling_design_anchor",
        ): "c53802e6ec2f7484c67b444bbc83c43bdfae28f8fd8414f21039055e2ad18eb1",
        (
            "s18_long_lead_equipment",
            "transformer_delivery_exposure",
        ): "1627486cc55c0f3a3c69b97bcdbb4975365a0ce7551483e9ea7b9c465e16cbc1",
        (
            "s18_long_lead_equipment",
            "turbine_manufacturing_slot",
        ): "49a27dc8d4ad7eac546f52ba4c8d81160edd0fd1cf960a9ed8e2cb7f59c66b7b",
        (
            "s18_long_lead_equipment",
            "turbine_slot_dependency",
        ): "10f00ccbad5fb03a193c35a7ab1868c621127060360eccb9d659f70214d8ed07",
        (
            "s18_long_lead_equipment",
            "cooling_product_availability_example",
        ): "ee0198b4a9d91fb4fc273e9d06afcb4b088175cefbfc3b4ff256423d73764356",
        (
            "s18_long_lead_equipment",
            "liquid_cooling_acceptance",
        ): "8bf81c0039133972694c6381577dd468f090a2286ad6993fd97caea3ae578441",
        (
            "s19_fast_load_slow_grid",
            "bess_future",
        ): "5de256c19f9104c0808eb624ba8915b93d476ece4fb2909438593493d253753d",
        (
            "s19_fast_load_slow_grid",
            "bess_operation_unknown",
        ): "f1161459a3cc8ef541a4c6c80cc3ab4f5bb8e2a236564a84b4c6039bb2d340ce",
        (
            "s19_fast_load_slow_grid",
            "operating_compute_anchor",
        ): "300de23c3a7ef43cfaf8634668860155a90d15a6732329fca2c4063c1696943b",
        (
            "s19_fast_load_slow_grid",
            "synchronized_ai_load_dynamics",
        ): "75778b2d598bb8fdd26be583d7d425ecbb0beb36f92b84421b5fda945b6e2bff",
        (
            "s19_fast_load_slow_grid",
            "voltage_sensitive_load_event",
        ): "42015a26ea8dd6852bbb824d6a0f086680ea897056b149eaff8934ae54f1be04",
        (
            "s19_fast_load_slow_grid",
            "ride_through_engineering_boundary",
        ): "e35d6cff6e8e37227edd72565cfbbff15c85d54e8dc017ad8b964b21fb025638",
        (
            "s19_fast_load_slow_grid",
            "operating_load_shaping_observations",
        ): "982d43e20a5f0492928e9ad16a871f4cea0f67e854cd9fdf89031762bc0225db",
        (
            "s19_fast_load_slow_grid",
            "abilene_transient_and_bess_boundary",
        ): "68b9e57c56551ff04058e53d634202eb08daf8362bf2f4d272ad022b1a06dbdf",
        (
            "s20_build_sequence",
            "planned_grid_boundary",
        ): "75dbde2e0ca56ccceee4f3e333bb6ff031a68f92b589c55e29abca3c15ffc9c8",
        (
            "s20_build_sequence",
            "infrastructure_milestones",
        ): "7a443dcf034c8194989624541c7d10dc151d2ec7df9a658d3f86ab7c8fb02086",
        (
            "s20_build_sequence",
            "energized_minimum",
        ): "7f8df0527e34996c09778adc2e759beac2a49e5eb4025b3505be9a22ac3bf8c8",
        (
            "s20_build_sequence",
            "installed_gpu_no_estimate",
        ): "7aae6e8d52f729005dda8736fee34ef0ca74ecb25e986c7e9932d9f6b1e74a6b",
        (
            "s20_build_sequence",
            "live_compute_boundary",
        ): "c3f1666fb4a865a0ebfe2d3b6c0fc541d57d453a0d0699acdc5569da1cac1d4c",
        (
            "s20_build_sequence",
            "untyped_delivery_boundary",
        ): "93890faa661992ee6107a565cef0937497b1f3b2a671d48a140e94e255af9580",
        (
            "s20_build_sequence",
            "construction_start",
        ): "eac894265b0bc6a8b4750743f2e60a287b391b5c692d8e546c22b7b63c8d08e9",
        (
            "s20_build_sequence",
            "first_two_buildings_energized",
        ): "3f8144d8fdfbf0f49941d0376a1c4b679adeaba3a905760465eee585e6216c37",
        (
            "s20_build_sequence",
            "first_phase_operational",
        ): "81bb92b6f698f7c55f8f864d5164cf0423225feb5be45a9a3c7aff938c1d36ee",
        (
            "s20_build_sequence",
            "remaining_buildings_plan",
        ): "b894d50d28fa884cb5a17e2e8b4f5b43dcd22f1fae0ba4b7e13f272576b7c8f7",
        (
            "s20_build_sequence",
            "current_delivery_boundary",
        ): "b395775c667661954b3d3c1d272477130f417f8bb24c1039beac55c441f30e51",
        (
            "s21_capital_ownership",
            "stargate_responsibility_structure",
        ): "e1917be6bd820238681d82d6c621a897227829ed4414d9a9c48390de54187225",
        (
            "s21_capital_ownership",
            "abilene_developer_roles",
        ): "06e684cadc98fdf81e30b7a24c42cf34733cb110568a04db08a8e2f398546c8f",
        (
            "s21_capital_ownership",
            "phase1_delivery_and_operations_contract",
        ): "5b377336e1e18a66bbcec7bceeec4d5d23395695c6c674c79021f4964e1b2dc1",
        (
            "s21_capital_ownership",
            "operating_compute_roles",
        ): "d2231e6bc7ddebf884a75263f6f37a112ccca6eb7b840a8884fd759ec431b4db",
        (
            "s21_capital_ownership",
            "legal_ownership_boundary",
        ): "c6e12909385af741afb308e72882144ea87a7d87417885a44f8082c18d8d4756",
        (
            "s22_capital_risk",
            "phase1_financing_and_lease",
        ): "816420c5cd6b62a4f52b7f8eb68a7b6de2dd6d206216f4bb750c60972c41d8fe",
        (
            "s22_capital_risk",
            "phase2_joint_venture",
        ): "1b4162b996613156276970c4d6ac986fc609ad301c4fe0b763a1ff309dc8837e",
        (
            "s22_capital_risk",
            "undisclosed_capital_and_risk_terms",
        ): "f66695e8375ffeb0ebc2475203e4c53618398cf0930840f33c31bad9090c4019",
        (
            "s23_business_models",
            "developer_role_comparison",
        ): "06e684cadc98fdf81e30b7a24c42cf34733cb110568a04db08a8e2f398546c8f",
        (
            "s23_business_models",
            "colocation_comparison",
        ): "15d1e8066e2d4b96b0cb0b49be68624acdd3b1c168d31b63583cf80f10d8bdea",
        (
            "s23_business_models",
            "neocloud_operating_comparison",
        ): "160e9a338fc76cb4e318f89cdaf8dbef566e0f742a14c317e333fc9dcdc26121",
        (
            "s23_business_models",
            "neocloud_contract_risk_comparison",
        ): "32e489ba49fd218320e25e259b15e17e37c3310e373a53defc435d378d12b99e",
        (
            "s23_business_models",
            "hyperscale_cloud_comparison",
        ): "335146e0bba1102a0fb999ca436fe6e1215f585d79ea02f3b7debd2810295554",
        (
            "s24_megawatts_to_tokens",
            "current_installed_gpu_no_estimate",
        ): "7aae6e8d52f729005dda8736fee34ef0ca74ecb25e986c7e9932d9f6b1e74a6b",
        (
            "s24_megawatts_to_tokens",
            "untyped_delivery_boundary",
        ): "93890faa661992ee6107a565cef0937497b1f3b2a671d48a140e94e255af9580",
        (
            "s24_megawatts_to_tokens",
            "operating_platform_anchor",
        ): "300de23c3a7ef43cfaf8634668860155a90d15a6732329fca2c4063c1696943b",
        (
            "s24_megawatts_to_tokens",
            "rack_power_product_reference",
        ): "a4832442a3a67866490cf1eef43c3b98019a12c082305f55b9d83118744cac2f",
        (
            "s24_megawatts_to_tokens",
            "selected_heat_rejection",
        ): "c53802e6ec2f7484c67b444bbc83c43bdfae28f8fd8414f21039055e2ad18eb1",
        (
            "s24_megawatts_to_tokens",
            "pue_accounting_boundary",
        ): "cb7d0e71a19d47a10d91625e54993c7a4eab61ada755e28632999279f7d24bc8",
        (
            "s24_megawatts_to_tokens",
            "facility_to_it_scenario_step",
        ): "38594581d014348ab72e549b40eee3ea78ad28b3f6c60285689ac757ed93bbf9",
        (
            "s24_megawatts_to_tokens",
            "rack_compute_product_reference",
        ): "4721b6540efb5edaa50e592fd094f46b3aa62d201e10ac2b902a7be1616cb66a",
        (
            "s24_megawatts_to_tokens",
            "training_published_method",
        ): "694e2de078dfc4b22d7b4dba398d3af37374f42be9b1269434145bbbe72caa76",
        (
            "s24_megawatts_to_tokens",
            "training_scenario_step",
        ): "d2ac679518f873bcf2fa2fde961b2f244eac2860131a7afa773a131a3f8c0885",
        (
            "s24_megawatts_to_tokens",
            "inference_published_boundaries",
        ): "7079c40b8eb93f89e51e2cab6e11591289f03bf0f6ec407328f37addc8dd620e",
        (
            "s24_megawatts_to_tokens",
            "inference_scenario_step",
        ): "e08f42bc378fe70ee90a6c99bd1d33894e9e967a9581e5a2adba9b7e60d0bbf2",
        (
            "s24_megawatts_to_tokens",
            "complete_scenario_recipe",
        ): "471c7f4d6f8a3496014c311736f6e69513981c21224da369bb9d9447e315c179",
        (
            "s24_megawatts_to_tokens",
            "site_power_no_estimates",
        ): "9b94a262458aaf2d90888849ec7b2ea5454ac5dad64dec6f64c72d9d193ae6bd",
        (
            "s24_megawatts_to_tokens",
            "site_compute_no_estimates",
        ): "fdb1eb523f9162134404c3c1140148caf5391e78a19fe01dd2f2fcfff63420e4",
        (
            "s24_megawatts_to_tokens",
            "site_workload_configuration_unknown",
        ): "2719a2b12dc9d7e6559be09f5060af388d6505f447cd4542dfdbfbb41aa83c3f",
    }
)
SEGMENT_TRANSITION_FIELDS = {"to", "cue"}
SEGMENT_READINESS = {"evidence_ready", "research_required"}
SEGMENT_CAMERA_STATUS = {"existing", "planned"}
SEGMENT_ASSERTIONS = {
    "accounting_reference",
    "anticipated",
    "business_model_reference",
    "confirmed",
    "confirmed_minimum",
    "contract_reference",
    "design_reference",
    "derived_scenario_reference",
    "excluded_scope",
    "explicit_unknown",
    "future_design",
    "live_by",
    "method_reference",
    "no_evidence_backed_estimate",
    "permitted",
    "planned",
    "product_reference",
    "reported_untyped",
    "reported_structure",
    "selected_design",
}
SEGMENT_CLAIM_BINDINGS = {"topology", "overlay"}
LEDGER_ID_PATTERN = re.compile(r"[a-z][a-z0-9_]*\Z")
ASSERTION_REQUIRED_GUARDS = {
    "accounting_reference": {"contractual_to_physical"},
    "anticipated": {"anticipated_to_measured"},
    "business_model_reference": {"contractual_to_physical"},
    "confirmed_minimum": {"minimum_to_exact"},
    "contract_reference": {"contractual_to_physical"},
    "design_reference": {"design_to_as_built"},
    "derived_scenario_reference": {
        "capacity_basis_substitution",
        "energy_power_time_basis",
        "power_to_compute_bridge",
        "scenario_to_site_estimate",
    },
    "excluded_scope": {"excluded_scope_addition"},
    "explicit_unknown": {"null_to_zero"},
    "future_design": {"future_design_to_operational"},
    "live_by": {"live_by_to_start_date"},
    "method_reference": {"capacity_basis_substitution"},
    "no_evidence_backed_estimate": {"null_to_zero"},
    "permitted": {"permitted_to_installed", "permitted_to_commissioned"},
    "planned": {"planned_to_operational"},
    "product_reference": {"product_to_site_configuration"},
    "reported_untyped": {"untyped_to_capacity"},
    "reported_structure": {"announced_to_operational"},
    "selected_design": {"design_to_as_built"},
}
BLOCKER_PLACEHOLDERS = {"research", "research required", "tbd", "todo", "unknown"}
PROMOTION_GUARDS = {
    "announced_to_operational",
    "anticipated_to_measured",
    "capacity_basis_substitution",
    "conceptual_to_as_built",
    "contractual_to_physical",
    "design_ceiling_to_installed",
    "design_to_as_built",
    "energy_power_time_basis",
    "excluded_scope_addition",
    "facility_financing_to_component_allocation",
    "future_design_to_operational",
    "live_by_to_start_date",
    "minimum_to_exact",
    "model_range_to_site_configuration",
    "market_example_to_site_schedule",
    "named_role_to_asset_assignment",
    "null_to_zero",
    "permitted_to_commissioned",
    "permitted_to_installed",
    "planned_to_operational",
    "product_to_site_configuration",
    "power_to_compute_bridge",
    "reverse_physical_flow",
    "single_path_conflation",
    "site_scope_transfer",
    "scenario_to_site_estimate",
    "substation_to_it_load",
    "untyped_to_capacity",
}


class ValidationError(ValueError):
    """Raised when any project contract is violated."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silent mapping-key replacement."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            mark = key_node.start_mark
            raise ValidationError(
                f"{mark.name}:{mark.line + 1}:{mark.column + 1}: unhashable YAML mapping key"
            ) from exc
        if duplicate:
            mark = key_node.start_mark
            raise ValidationError(
                f"{mark.name}:{mark.line + 1}:{mark.column + 1}: duplicate YAML key {key!r}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _load_yaml_strict(path: Path) -> dict[str, Any]:
    try:
        with path.open() as stream:
            data = yaml.load(stream, Loader=_UniqueKeyLoader)
    except ValidationError:
        raise
    except (OSError, yaml.YAMLError) as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: expected a mapping")
    return data


def _unique(items: Iterable[str], location: str) -> set[str]:
    values = list(items)
    if len(values) != len(set(values)):
        raise ValidationError(f"{location}: IDs must be unique")
    return set(values)


def _exact_fields(record: dict[str, Any], fields: set[str], location: str) -> None:
    missing = fields - set(record)
    extra = set(record) - fields
    if missing or extra:
        raise ValidationError(
            f"{location}: missing={sorted(missing)} extra={sorted(extra)}"
        )


def _required_known_fields(
    record: dict[str, Any],
    required_fields: set[str],
    known_fields: set[str],
    location: str,
) -> None:
    missing = required_fields - set(record)
    extra = set(record) - known_fields
    if missing or extra:
        raise ValidationError(
            f"{location}: missing={sorted(missing)} extra={sorted(extra, key=repr)}"
        )


def _nonempty_string(value: Any, location: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{location}: expected a non-empty string")


def _validate_fact_value_kind(value: Any, unit: Any, location: str) -> None:
    if unit is not None:
        _nonempty_string(unit, f"{location}.unit")
    if unit not in FACT_UNIT_VALUE_KIND:
        raise ValidationError(f"{location}.unit: unknown fact unit {unit!r}")
    if value is None:
        return
    if type(value) not in (str, bool, int, float):
        raise ValidationError(
            f"{location}.value: expected a scalar string, number, boolean, or null"
        )

    expected_kind = FACT_UNIT_VALUE_KIND[unit]
    if expected_kind == "number":
        if type(value) not in (int, float):
            raise ValidationError(
                f"{location}.value: unit {unit!r} requires a finite number"
            )
        if isinstance(value, float) and not math.isfinite(value):
            raise ValidationError(
                f"{location}.value: unit {unit!r} requires a finite number"
            )
    elif expected_kind == "boolean":
        if type(value) is not bool:
            raise ValidationError(f"{location}.value: unit {unit!r} requires a boolean")
    elif type(value) is not str or not value.strip():
        raise ValidationError(
            f"{location}.value: unit {unit!r} requires a non-empty string"
        )


def _contract_digest(values: Iterable[Any]) -> str:
    payload = json.dumps(
        list(values),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _ledger_context_digest(evidence: dict[str, Any]) -> str:
    context = []
    for field in LEDGER_CONTEXT_FIELDS:
        value = evidence[field]
        if isinstance(value, dict):
            value = sorted(value.items())
        context.append((field, value))
    return _contract_digest(context)


def _validate_ledger_context_contract_entry(
    ledger_id: str, evidence: dict[str, Any]
) -> None:
    expected_digest = LEDGER_CONTEXT_CONTRACT.get(ledger_id)
    if expected_digest is None:
        raise ValidationError(
            f"immutable ledger context contract has no ledger {ledger_id!r}"
        )
    if _ledger_context_digest(evidence) != expected_digest:
        raise ValidationError(
            f"evidence ledger {ledger_id}: immutable ledger context contract "
            f"requires exact {LEDGER_CONTEXT_FIELDS!r}; schema_version, subject, "
            "accessed_as_of, and evidence_boundary changes require an explicit "
            "provenance-qualified contract update"
        )


def _validate_registered_ledger_context_contract(
    evidence_ledgers: dict[str, dict[str, Any]],
) -> None:
    expected_ids = set(LEDGER_CONTEXT_CONTRACT)
    actual_ids = set(evidence_ledgers)
    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids
    if missing or extra:
        raise ValidationError(
            "immutable ledger context contract ledger mismatch: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )


def _source_payload_digest(source: dict[str, Any]) -> str:
    return _contract_digest(source[field] for field in SOURCE_PAYLOAD_FIELDS)


def _source_payload_contract_for_ledger(ledger_id: str) -> dict[str, str]:
    prefix = f"{ledger_id}:"
    return {
        qualified_id.removeprefix(prefix): digest
        for qualified_id, digest in SOURCE_PAYLOAD_CONTRACT.items()
        if qualified_id.startswith(prefix)
    }


def _validate_ledger_source_identity_contract(
    ledger_id: str, evidence: dict[str, Any]
) -> None:
    expected = _source_payload_contract_for_ledger(ledger_id)
    sources = evidence.get("sources")
    if not expected:
        raise ValidationError(
            f"immutable source payload contract has no ledger {ledger_id!r}"
        )
    if not isinstance(sources, dict):
        raise ValidationError(
            f"evidence ledger {ledger_id}.sources: expected a mapping"
        )
    missing = set(expected) - set(sources)
    extra = set(sources) - set(expected)
    if missing or extra:
        raise ValidationError(
            f"immutable source payload contract mismatch for ledger {ledger_id!r}: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )


def _validate_source_payload_contract_entry(
    ledger_id: str, source_id: str, source: dict[str, Any]
) -> None:
    expected_digest = _source_payload_contract_for_ledger(ledger_id)[source_id]
    if _source_payload_digest(source) != expected_digest:
        raise ValidationError(
            f"evidence ledger {ledger_id}.sources.{source_id}: immutable source "
            f"payload contract requires exact {SOURCE_PAYLOAD_FIELDS!r}; "
            "a change requires a provenance-qualified contract update"
        )


def _validate_ledger_source_payload_contract(
    ledger_id: str, evidence: dict[str, Any]
) -> None:
    _validate_ledger_source_identity_contract(ledger_id, evidence)
    for source_id, source in evidence["sources"].items():
        _validate_source_payload_contract_entry(ledger_id, source_id, source)


def _fact_payload_digest(fact: dict[str, Any]) -> str:
    return _contract_digest(fact[field] for field in FACT_PAYLOAD_FIELDS)


def _fact_contract_for_ledger(ledger_id: str) -> dict[str, tuple[Any, str]]:
    prefix = f"{ledger_id}:"
    return {
        qualified_id.removeprefix(prefix): contract
        for qualified_id, contract in FACT_IDENTITY_CONTRACT.items()
        if qualified_id.startswith(prefix)
    }


def _validate_ledger_fact_identity_contract(
    ledger_id: str, evidence: dict[str, Any]
) -> None:
    expected = _fact_contract_for_ledger(ledger_id)
    facts = evidence.get("facts")
    if not expected:
        raise ValidationError(
            f"immutable fact identity contract has no ledger {ledger_id!r}"
        )
    if not isinstance(facts, dict):
        raise ValidationError(f"evidence ledger {ledger_id}.facts: expected a mapping")
    actual_ids = set(facts)
    expected_ids = set(expected)
    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids
    if missing or extra:
        raise ValidationError(
            f"immutable fact identity contract mismatch for ledger {ledger_id!r}: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )
    for fact_id, (expected_unit, expected_kind) in expected.items():
        fact = facts[fact_id]
        actual_unit = fact["unit"]
        actual_kind = FACT_UNIT_VALUE_KIND[actual_unit]
        if actual_unit != expected_unit or actual_kind != expected_kind:
            raise ValidationError(
                f"evidence ledger {ledger_id}.facts.{fact_id}: immutable fact "
                f"identity requires unit={expected_unit!r} kind={expected_kind!r}; "
                f"got unit={actual_unit!r} kind={actual_kind!r}"
            )


def _numeric_minimum_contract_for_ledger(ledger_id: str) -> dict[str, int | float]:
    prefix = f"{ledger_id}:"
    return {
        qualified_id.removeprefix(prefix): minimum
        for qualified_id, minimum in FACT_NUMERIC_MINIMUM_CONTRACT.items()
        if qualified_id.startswith(prefix)
    }


def _validate_ledger_numeric_minimum_contract(
    ledger_id: str, evidence: dict[str, Any]
) -> None:
    expected = _numeric_minimum_contract_for_ledger(ledger_id)
    facts = evidence["facts"]
    for fact_id, minimum in expected.items():
        value = facts[fact_id]["value"]
        if value is None:
            continue
        if type(value) not in (int, float) or (
            isinstance(value, float) and not math.isfinite(value)
        ):
            raise ValidationError(
                f"evidence ledger {ledger_id}.facts.{fact_id}.value: numeric "
                "minimum contract requires a finite number"
            )
        if value < minimum:
            raise ValidationError(
                f"evidence ledger {ledger_id}.facts.{fact_id}.value: numeric "
                f"minimum contract requires value >= {minimum}; got {value}"
            )


def _semantic_contract_for_ledger(
    ledger_id: str,
) -> dict[str, tuple[bool, str, str]]:
    prefix = f"{ledger_id}:"
    return {
        qualified_id.removeprefix(prefix): contract
        for qualified_id, contract in FACT_SEMANTIC_CONTRACT.items()
        if qualified_id.startswith(prefix)
    }


def _validate_ledger_fact_semantic_contract(
    ledger_id: str, evidence: dict[str, Any]
) -> None:
    expected = _semantic_contract_for_ledger(ledger_id)
    facts = evidence["facts"]
    for fact_id, expected_semantics in expected.items():
        fact = facts[fact_id]
        actual_semantics = (
            fact["value"] is None,
            fact["posture"],
            fact["lifecycle"],
        )
        if actual_semantics != expected_semantics:
            expected_null, expected_posture, expected_lifecycle = expected_semantics
            actual_null, actual_posture, actual_lifecycle = actual_semantics
            raise ValidationError(
                f"evidence ledger {ledger_id}.facts.{fact_id}: immutable fact "
                "semantic contract requires "
                f"value_is_null={expected_null!r} posture={expected_posture!r} "
                f"lifecycle={expected_lifecycle!r}; got "
                f"value_is_null={actual_null!r} posture={actual_posture!r} "
                f"lifecycle={actual_lifecycle!r}"
            )


def _fact_payload_contract_for_ledger(ledger_id: str) -> dict[str, str]:
    prefix = f"{ledger_id}:"
    return {
        qualified_id.removeprefix(prefix): digest
        for qualified_id, digest in FACT_PAYLOAD_CONTRACT.items()
        if qualified_id.startswith(prefix)
    }


def _validate_ledger_fact_payload_contract(
    ledger_id: str, evidence: dict[str, Any]
) -> None:
    expected = _fact_payload_contract_for_ledger(ledger_id)
    facts = evidence["facts"]
    for fact_id, expected_digest in expected.items():
        actual_digest = _fact_payload_digest(facts[fact_id])
        if actual_digest != expected_digest:
            raise ValidationError(
                f"evidence ledger {ledger_id}.facts.{fact_id}: immutable fact "
                f"payload contract requires exact {FACT_PAYLOAD_FIELDS!r}; "
                "a change requires a provenance-qualified contract update"
            )


def _validate_registered_fact_identity_contract(
    evidence_ledgers: dict[str, dict[str, Any]],
) -> None:
    expected_ledger_ids = {
        qualified_id.split(":", 1)[0] for qualified_id in FACT_IDENTITY_CONTRACT
    }
    actual_ledger_ids = set(evidence_ledgers)
    missing_ledgers = expected_ledger_ids - actual_ledger_ids
    extra_ledgers = actual_ledger_ids - expected_ledger_ids
    if missing_ledgers or extra_ledgers:
        raise ValidationError(
            "immutable fact identity contract ledger mismatch: "
            f"missing={sorted(missing_ledgers)} extra={sorted(extra_ledgers)}"
        )
    source_contract_ledger_ids = {
        qualified_id.split(":", 1)[0] for qualified_id in SOURCE_PAYLOAD_CONTRACT
    }
    if source_contract_ledger_ids != expected_ledger_ids:
        raise ValidationError(
            "immutable source payload contract ledger mismatch: "
            f"missing={sorted(expected_ledger_ids - source_contract_ledger_ids)} "
            f"extra={sorted(source_contract_ledger_ids - expected_ledger_ids)}"
        )
    actual_qualified_ids = {
        f"{ledger_id}:{fact_id}"
        for ledger_id, evidence in evidence_ledgers.items()
        for fact_id in (evidence.get("facts") or {})
    }
    expected_qualified_ids = set(FACT_IDENTITY_CONTRACT)
    semantic_qualified_ids = set(FACT_SEMANTIC_CONTRACT)
    if semantic_qualified_ids != expected_qualified_ids:
        raise ValidationError(
            "immutable fact semantic contract identity mismatch: "
            f"missing={sorted(expected_qualified_ids - semantic_qualified_ids)} "
            f"extra={sorted(semantic_qualified_ids - expected_qualified_ids)}"
        )
    payload_qualified_ids = set(FACT_PAYLOAD_CONTRACT)
    if payload_qualified_ids != expected_qualified_ids:
        raise ValidationError(
            "immutable fact payload contract identity mismatch: "
            f"missing={sorted(expected_qualified_ids - payload_qualified_ids)} "
            f"extra={sorted(payload_qualified_ids - expected_qualified_ids)}"
        )
    missing = expected_qualified_ids - actual_qualified_ids
    extra = actual_qualified_ids - expected_qualified_ids
    if missing or extra:
        raise ValidationError(
            "immutable registered fact identity contract mismatch: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )
    for ledger_id, evidence in evidence_ledgers.items():
        _validate_ledger_fact_identity_contract(ledger_id, evidence)


def _string_list(value: Any, location: str, *, allow_empty: bool = True) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValidationError(f"{location}: expected a list of strings")
    if not allow_empty and not value:
        raise ValidationError(f"{location}: expected a non-empty list")
    return _unique(value, location)


def _course_ledger_registry(
    meta: dict[str, Any], *, require_existing: bool = False
) -> dict[str, Path]:
    registry = meta.get("evidence_ledgers")
    if not isinstance(registry, dict) or not registry:
        raise ValidationError(
            "course.meta.evidence_ledgers must be a non-empty mapping"
        )

    evidence_root = (ROOT / "evidence").resolve()
    paths: dict[str, Path] = {}
    for ledger_id, raw_path in registry.items():
        if not isinstance(ledger_id, str) or not LEDGER_ID_PATTERN.fullmatch(ledger_id):
            raise ValidationError(
                f"course evidence ledger ID {ledger_id!r} must match {LEDGER_ID_PATTERN.pattern!r}"
            )
        _nonempty_string(raw_path, f"course.meta.evidence_ledgers.{ledger_id}")
        relative_path = Path(raw_path)
        if relative_path.is_absolute() or relative_path.suffix not in {".yaml", ".yml"}:
            raise ValidationError(
                f"course evidence ledger {ledger_id}: path must be a relative YAML file under evidence/"
            )
        resolved = (ROOT / relative_path).resolve()
        if resolved.parent != evidence_root and evidence_root not in resolved.parents:
            raise ValidationError(
                f"course evidence ledger {ledger_id}: path must remain under evidence/"
            )
        if require_existing and not resolved.is_file():
            raise ValidationError(
                f"course evidence ledger {ledger_id}: file does not exist: {raw_path}"
            )
        paths[ledger_id] = resolved

    if len(set(paths.values())) != len(paths):
        raise ValidationError("course evidence ledger paths must be unique")
    master_ledger = meta.get("master_evidence_ledger")
    if master_ledger not in paths:
        raise ValidationError(
            "course.meta.master_evidence_ledger must name a registered evidence ledger"
        )
    return paths


def _load_course_evidence_ledgers(course: dict[str, Any]) -> dict[str, dict[str, Any]]:
    meta = course.get("meta")
    if not isinstance(meta, dict):
        raise ValidationError("course.meta: expected a mapping")
    paths = _course_ledger_registry(meta, require_existing=True)
    ledgers = {ledger_id: _load_yaml_strict(path) for ledger_id, path in paths.items()}
    _validate_registered_ledger_context_contract(ledgers)
    for ledger_id, ledger in ledgers.items():
        _validate_evidence_schema(
            ledger,
            f"evidence ledger {ledger_id}",
            ledger_id=ledger_id,
        )
    _validate_registered_fact_identity_contract(ledgers)
    return ledgers


def _resolve_fact_ref(
    fact_ref: str,
    ledgers: dict[str, dict[str, Any]],
    location: str,
) -> tuple[str, str, dict[str, Any]]:
    if not isinstance(fact_ref, str) or fact_ref.count(":") != 1:
        raise ValidationError(
            f"{location}: malformed qualified fact reference {fact_ref!r}"
        )
    ledger_id, fact_id = fact_ref.split(":", 1)
    if not LEDGER_ID_PATTERN.fullmatch(ledger_id) or not LEDGER_ID_PATTERN.fullmatch(
        fact_id
    ):
        raise ValidationError(
            f"{location}: malformed qualified fact reference {fact_ref!r}"
        )
    if ledger_id not in ledgers:
        raise ValidationError(f"{location}: unknown evidence ledger {ledger_id!r}")
    facts = ledgers[ledger_id].get("facts") or {}
    if fact_id not in facts:
        raise ValidationError(f"{location}: unknown fact {fact_ref!r}")
    return ledger_id, fact_id, facts[fact_id]


def _source_refs(
    records: Iterable[dict[str, Any]], source_ids: set[str], location: str
) -> None:
    for record in records:
        unknown = set(record.get("source_ids") or []) - source_ids
        if unknown:
            raise ValidationError(
                f"{location} {record.get('id', '<record>')}: unknown sources {sorted(unknown)}"
            )


def _validate_fact_binding(
    record: dict[str, Any], facts: dict[str, dict[str, Any]], location: str
) -> None:
    record_id = record.get("id", "<record>")
    fact_ids = record.get("fact_ids")
    if not isinstance(fact_ids, list) or any(
        not isinstance(fact_id, str) for fact_id in fact_ids
    ):
        raise ValidationError(
            f"{location} {record_id}: fact_ids must be a list of strings"
        )
    _unique(fact_ids, f"{location} {record_id}.fact_ids")

    lifecycle = record["lifecycle"]
    if not fact_ids and lifecycle not in EMPTY_FACT_IDS_ALLOWED:
        raise ValidationError(
            f"{location} {record_id}: lifecycle {lifecycle!r} requires at least one fact_id"
        )

    unknown = set(fact_ids) - set(facts)
    if unknown:
        raise ValidationError(
            f"{location} {record_id}: unknown facts {sorted(unknown)}"
        )

    referenced = [facts[fact_id] for fact_id in fact_ids]
    expected_sources = {
        source_id for fact in referenced for source_id in fact.get("source_ids") or []
    }
    source_list = record.get("source_ids")
    if not isinstance(source_list, list) or any(
        not isinstance(source_id, str) for source_id in source_list
    ):
        raise ValidationError(
            f"{location} {record_id}: source_ids must be a list of strings"
        )
    _unique(source_list, f"{location} {record_id}.source_ids")
    actual_sources = set(source_list)
    if actual_sources != expected_sources:
        raise ValidationError(
            f"{location} {record_id}: source_ids must equal fact source union; "
            f"expected {sorted(expected_sources)}, got {sorted(actual_sources)}"
        )

    if lifecycle in OPERATIONAL_MASTER_LIFECYCLES:
        incompatible = [
            fact_id
            for fact_id, fact in zip(fact_ids, referenced)
            if fact.get("value") is None
            or fact.get("lifecycle") not in OPERATIONAL_ALLOWED_FACT_LIFECYCLES
        ]
        if incompatible:
            raise ValidationError(
                f"{location} {record_id}: facts {incompatible} cannot support "
                f"{lifecycle}; operational geometry cannot use null, design, "
                "product, permit, planned, or unknown evidence"
            )
        if not any(
            fact.get("lifecycle") in OPERATIONAL_FACT_LIFECYCLES for fact in referenced
        ):
            raise ValidationError(
                f"{location} {record_id}: {lifecycle} requires at least one "
                f"{sorted(OPERATIONAL_FACT_LIFECYCLES)} fact"
            )

    if lifecycle == "permitted" and not any(
        fact.get("lifecycle") == "permitted" for fact in referenced
    ):
        raise ValidationError(
            f"{location} {record_id}: permitted geometry requires a permitted fact"
        )

    if lifecycle == "future_design" and not any(
        fact.get("lifecycle") in DESIGN_FACT_LIFECYCLES for fact in referenced
    ):
        raise ValidationError(
            f"{location} {record_id}: future_design geometry requires a design fact"
        )


def _copy_ids(layout: dict[str, Any]) -> list[str]:
    ids = [layout["title_id"], layout["subtitle_id"]]
    ids.extend(zone["copy_id"] for zone in layout.get("zones") or [])
    ids.extend(
        region["copy_id"]
        for region in layout.get("regions") or []
        if "copy_id" in region
    )
    ids.extend(item["id"] for item in layout.get("room_labels") or [])
    ids.extend(item["id"] for item in layout.get("labels") or [])
    legend = layout.get("legend") or {}
    if legend:
        ids.append(legend["title_id"])
        ids.extend(item["id"] for item in legend.get("entries") or [])
    return ids


def _validate_evidence_schema(
    evidence: dict[str, Any],
    location: str = "evidence",
    *,
    ledger_id: str | None = None,
) -> tuple[set[str], set[str]]:
    if not isinstance(evidence, dict):
        raise ValidationError(f"{location}: expected a mapping")
    _exact_fields(evidence, EVIDENCE_FIELDS, location)
    if (
        type(evidence.get("schema_version")) is not int
        or evidence["schema_version"] != 1
    ):
        raise ValidationError(f"{location}: schema_version must be 1")
    if not isinstance(evidence.get("subject"), dict) or not evidence["subject"]:
        raise ValidationError(f"{location}.subject: expected a non-empty mapping")
    _required_known_fields(
        evidence["subject"],
        SUBJECT_REQUIRED_FIELDS,
        SUBJECT_FIELDS,
        f"{location}.subject",
    )
    for field, value in evidence["subject"].items():
        _nonempty_string(value, f"{location}.subject.{field}")
    _nonempty_string(evidence.get("accessed_as_of"), f"{location}.accessed_as_of")
    if (
        not isinstance(evidence.get("evidence_boundary"), dict)
        or not evidence["evidence_boundary"]
    ):
        raise ValidationError(
            f"{location}.evidence_boundary: expected a non-empty mapping"
        )
    _required_known_fields(
        evidence["evidence_boundary"],
        EVIDENCE_BOUNDARY_REQUIRED_FIELDS,
        EVIDENCE_BOUNDARY_FIELDS,
        f"{location}.evidence_boundary",
    )
    for field, value in evidence["evidence_boundary"].items():
        _nonempty_string(value, f"{location}.evidence_boundary.{field}")
    if ledger_id is not None:
        _validate_ledger_context_contract_entry(ledger_id, evidence)
    sources = evidence["sources"]
    facts = evidence["facts"]
    if not isinstance(sources, dict) or not sources:
        raise ValidationError(f"{location}.sources: expected a non-empty mapping")
    if not isinstance(facts, dict) or not facts:
        raise ValidationError(f"{location}.facts: expected a non-empty mapping")
    source_ids = _unique(sources, f"{location}.sources")
    fact_ids = _unique(facts, f"{location}.facts")
    if ledger_id is not None:
        _validate_ledger_source_identity_contract(ledger_id, evidence)
    for source_id, source in sources.items():
        source_location = f"{location}.sources.{source_id}"
        _nonempty_string(source_id, source_location)
        if not isinstance(source, dict):
            raise ValidationError(f"{source_location}: expected a mapping")
        _exact_fields(source, SOURCE_FIELDS, source_location)
        for field in (
            "publisher",
            "title",
            "kind",
            "url",
            "accessed_as_of",
            "date_note",
        ):
            _nonempty_string(source[field], f"{source_location}.{field}")
        for field in ("publication_date", "review_date"):
            if source[field] is not None:
                _nonempty_string(source[field], f"{source_location}.{field}")
        if not source["kind"].startswith("primary_"):
            raise ValidationError(
                f"{source_location}.kind: expected a primary-source kind"
            )
        if not source["url"].startswith("https://"):
            raise ValidationError(
                f"{source_location}: expected an HTTPS primary-source URL"
            )
        if ledger_id is not None:
            _validate_source_payload_contract_entry(ledger_id, source_id, source)
        if source["accessed_as_of"] != evidence["accessed_as_of"]:
            raise ValidationError(
                f"{source_location}: accessed_as_of must match the evidence ledger"
            )
    for fact_id, fact in facts.items():
        fact_location = f"{location}.facts.{fact_id}"
        _nonempty_string(fact_id, fact_location)
        if not isinstance(fact, dict):
            raise ValidationError(f"{fact_location}: expected a mapping")
        _exact_fields(fact, FACT_FIELDS, fact_location)
        for field in ("scope", "basis", "lifecycle", "as_of", "posture"):
            _nonempty_string(fact[field], f"{fact_location}.{field}")
        if fact["lifecycle"] not in FACT_LIFECYCLES:
            raise ValidationError(
                f"{fact_location}: unknown lifecycle {fact['lifecycle']!r}"
            )
        if fact["posture"] not in FACT_POSTURES:
            raise ValidationError(
                f"{fact_location}: unknown posture {fact['posture']!r}"
            )
        _validate_fact_value_kind(fact["value"], fact["unit"], fact_location)
        if not isinstance(fact["source_ids"], list) or not fact["source_ids"]:
            raise ValidationError(
                f"{fact_location}: source_ids must be a non-empty list"
            )
        if any(
            not isinstance(source_id, str) or not source_id.strip()
            for source_id in fact["source_ids"]
        ):
            raise ValidationError(
                f"{fact_location}.source_ids: expected non-empty strings"
            )
        _unique(fact["source_ids"], f"{fact_location}.source_ids")
        unknown = set(fact["source_ids"]) - source_ids
        if unknown:
            raise ValidationError(f"{fact_location}: unknown sources {sorted(unknown)}")
        if fact["value"] is None and fact["posture"] not in NULL_POSTURES:
            raise ValidationError(
                f"{fact_location}: null value requires one of {sorted(NULL_POSTURES)}"
            )
        if fact["value"] is not None and fact["posture"] in NULL_POSTURES:
            raise ValidationError(
                f"{fact_location}: null posture requires a null value"
            )
    if ledger_id is not None:
        _validate_ledger_fact_identity_contract(ledger_id, evidence)
        _validate_ledger_numeric_minimum_contract(ledger_id, evidence)
        _validate_ledger_fact_semantic_contract(ledger_id, evidence)
        _validate_ledger_fact_payload_contract(ledger_id, evidence)
    return source_ids, fact_ids


def _validate_abilene_evidence(evidence: dict[str, Any]) -> None:
    if evidence.get("accessed_as_of") != "2026-08-25":
        raise ValidationError("Abilene evidence accessed_as_of must be 2026-08-25")
    facts = evidence["facts"]
    gpu = facts["installed_gpu_count"]
    if gpu["value"] is not None or gpu["basis"] != "no evidence-backed estimate":
        raise ValidationError(
            "installed_gpu_count must fail closed with literal no evidence-backed estimate"
        )
    if facts["adjacent_microsoft_scope_included"]["value"] is not False:
        raise ValidationError("adjacent Microsoft scope must remain excluded")
    for null_fact in (
        "campus_lpt_secondary_as_built_voltage_kv",
        "grid_expansion_upstream_line",
        "gas_commissioned_mw",
        "diesel_units_installed",
        "diesel_operational_units",
        "operational_buildings_exact",
        "exact_workload_start_date",
        "rack_power_shelf_ac_input_voltage_v",
        "generator_terminal_site_voltage_kv",
        "cooling_measured_operating_consumption_gallons",
        "bess_operational_status",
        "campus_source_merge_as_built_topology",
        "bess_campus_connection_as_built_topology",
        "diesel_campus_connection_as_built_topology",
    ):
        if facts[null_fact]["value"] is not None:
            raise ValidationError(
                f"{null_fact} must remain null until new primary evidence is added"
            )


def _validate_evidence(evidence: dict[str, Any]) -> tuple[set[str], set[str]]:
    source_ids, fact_ids = _validate_evidence_schema(evidence, ledger_id="abilene")
    _validate_abilene_evidence(evidence)
    return source_ids, fact_ids


def _validate_master_schema(master: dict[str, Any]) -> None:
    if not isinstance(master, dict):
        raise ValidationError("master: expected a mapping")
    _exact_fields(master, MASTER_FIELDS, "master")

    meta = master["meta"]
    if not isinstance(meta, dict):
        raise ValidationError("master.meta: expected a mapping")
    _exact_fields(meta, MASTER_META_FIELDS, "master.meta")
    if type(meta["version"]) is not int or meta["version"] != 1:
        raise ValidationError("master.meta.version must be the integer 1")
    for field in ("status", "evidence_file", "diagram_posture"):
        _nonempty_string(meta[field], f"master.meta.{field}")
    if type(meta["reference_as_of"]) is not date:
        raise ValidationError("master.meta.reference_as_of: expected an exact date")

    journey = meta["journey"]
    if not isinstance(journey, dict):
        raise ValidationError("master.meta.journey: expected a mapping")
    _exact_fields(journey, MASTER_JOURNEY_FIELDS, "master.meta.journey")
    electrical_journey = journey["electrical"]
    if not isinstance(electrical_journey, dict):
        raise ValidationError("master.meta.journey.electrical: expected a mapping")
    _exact_fields(
        electrical_journey,
        MASTER_ELECTRICAL_JOURNEY_FIELDS,
        "master.meta.journey.electrical",
    )
    for journey_id, values in electrical_journey.items():
        _string_list(
            values,
            f"master.meta.journey.electrical.{journey_id}",
            allow_empty=False,
        )
    _string_list(
        journey["thermal"],
        "master.meta.journey.thermal",
        allow_empty=False,
    )

    journey_bar = meta["journey_bar"]
    if not isinstance(journey_bar, dict):
        raise ValidationError("master.meta.journey_bar: expected a mapping")
    _exact_fields(
        journey_bar,
        MASTER_JOURNEY_BAR_FIELDS,
        "master.meta.journey_bar",
    )
    for journey_id, values in journey_bar.items():
        _string_list(
            values,
            f"master.meta.journey_bar.{journey_id}",
            allow_empty=False,
        )
    _string_list(
        meta["gigawatts_to_tokens_funnel"],
        "master.meta.gigawatts_to_tokens_funnel",
        allow_empty=False,
    )

    reference_campus = master["reference_campus"]
    if not isinstance(reference_campus, dict):
        raise ValidationError("master.reference_campus: expected a mapping")
    _exact_fields(
        reference_campus,
        MASTER_REFERENCE_CAMPUS_FIELDS,
        "master.reference_campus",
    )
    for field, value in reference_campus.items():
        _nonempty_string(value, f"master.reference_campus.{field}")

    status_styles = master["status_styles"]
    if not isinstance(status_styles, dict):
        raise ValidationError("master.status_styles: expected a mapping")
    _exact_fields(status_styles, MASTER_STATUS_STYLE_IDS, "master.status_styles")
    for style_id, style in status_styles.items():
        location = f"master.status_styles.{style_id}"
        if not isinstance(style, dict):
            raise ValidationError(f"{location}: expected a mapping")
        expected_fields = set(MASTER_STATUS_STYLE_FIELDS)
        if style_id == "course_variant":
            expected_fields.add("not an Abilene fact")
        _exact_fields(style, expected_fields, location)
        _nonempty_string(style["line"], f"{location}.line")
        _nonempty_string(style["meaning"], f"{location}.meaning")
        if style_id == "course_variant" and style["not an Abilene fact"] is not None:
            raise ValidationError(
                "master.status_styles.course_variant.not an Abilene fact "
                "must remain null"
            )

    copy = master["copy"]
    if not isinstance(copy, dict) or not copy:
        raise ValidationError("master.copy: expected a non-empty mapping")
    allowed_copy_field_sets = {
        frozenset(MASTER_COPY_TEXT_FIELDS),
        frozenset(MASTER_COPY_HIDDEN_TEXT_FIELDS),
        frozenset(MASTER_COPY_TEMPLATE_FIELDS),
        frozenset(MASTER_COPY_UNKNOWN_TEMPLATE_FIELDS),
    }
    for copy_id, spec in copy.items():
        location = f"master.copy.{copy_id}"
        _nonempty_string(copy_id, location)
        if not isinstance(spec, dict):
            raise ValidationError(f"{location}: expected a mapping")
        if frozenset(spec) not in allowed_copy_field_sets:
            raise ValidationError(
                f"{location}: copy must use exactly text or template+facts; "
                f"fields={sorted(spec)}"
            )
        if "text" in spec:
            _nonempty_string(spec["text"], f"{location}.text")
            if "base_visible" in spec and spec["base_visible"] is not False:
                raise ValidationError(f"{location}.base_visible must be false")
            continue
        _nonempty_string(spec["template"], f"{location}.template")
        _string_list(spec["facts"], f"{location}.facts", allow_empty=False)
        if "posture" in spec and spec["posture"] != "explicit_unknown":
            raise ValidationError(
                f"{location}.posture must be 'explicit_unknown' when present"
            )


def _validate_topology_presence_contract(
    nodes: list[dict[str, Any]], edges: list[dict[str, Any]]
) -> None:
    qualified_records = [
        (f"{kind}:{record['id']}", record)
        for kind, records in (("node", nodes), ("edge", edges))
        for record in records
    ]
    qualified_ids = [qualified_id for qualified_id, _ in qualified_records]
    _unique(qualified_ids, "master topology identities")
    actual_ids = set(qualified_ids)
    expected_ids = set(TOPOLOGY_PRESENCE_CONTRACT)
    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids
    if missing or extra:
        raise ValidationError(
            "immutable topology presence contract mismatch: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )
    for qualified_id, record in qualified_records:
        expected_presence = TOPOLOGY_PRESENCE_CONTRACT[qualified_id]
        if record["presence"] != expected_presence:
            raise ValidationError(
                f"master topology {qualified_id}: immutable presence contract "
                f"requires {expected_presence!r}; got {record['presence']!r}"
            )


def _validate_topology_posture(
    record: dict[str, Any], location: str, *, kind: str
) -> None:
    presence = record["presence"]
    lifecycle = record["lifecycle"]
    allowed_lifecycles = (
        NODE_PRESENCE_LIFECYCLES if kind == "node" else EDGE_PRESENCE_LIFECYCLES
    )[presence]
    if lifecycle not in allowed_lifecycles:
        raise ValidationError(
            f"{location}: presence {presence!r} is incompatible with lifecycle "
            f"{lifecycle!r}; expected one of {sorted(allowed_lifecycles)}"
        )

    source_ids = record["source_ids"]
    fact_ids = record["fact_ids"]
    if presence in EVIDENCED_PRESENCES and (not source_ids or not fact_ids):
        raise ValidationError(
            f"{location}: presence {presence!r} requires non-empty source_ids "
            "and fact_ids"
        )
    if presence in {"course_variant", "physical_sink"} and (source_ids or fact_ids):
        raise ValidationError(
            f"{location}: presence {presence!r} cannot own evidence bindings"
        )

    base_visible = record.get("base_visible", True)
    if presence == "course_variant" and base_visible is not False:
        raise ValidationError(f"{location}: course_variant must be base-hidden")
    if presence != "course_variant" and base_visible is not True:
        raise ValidationError(
            f"{location}: only course_variant records may be base-hidden"
        )

    if kind == "node":
        if (presence == "physical_sink") != (lifecycle == "terminal"):
            raise ValidationError(
                f"{location}: physical_sink presence and terminal lifecycle "
                "must occur together"
            )
        if (
            presence in {"course_variant", "physical_sink"}
            and record["as_of"] is not None
        ):
            raise ValidationError(
                f"{location}: {presence} must not claim an as-of date"
            )
        return

    normal_state = record["normal_state"]
    flow_direction = record["flow_direction"]
    if presence == "course_variant":
        if normal_state != "not_physical" or flow_direction != "none":
            raise ValidationError(
                f"{location}: course_variant edges require "
                "normal_state='not_physical' and flow_direction='none'"
            )
        return
    if normal_state == "not_physical" or flow_direction == "none":
        raise ValidationError(
            f"{location}: physical teaching/evidence edges cannot use a "
            "not-physical state or no-flow direction"
        )
    if (normal_state == "available_if_built") != (lifecycle == "permitted"):
        raise ValidationError(
            f"{location}: available_if_built state and permitted lifecycle "
            "must occur together"
        )


def _validate_master(
    master: dict[str, Any], evidence: dict[str, Any], source_ids: set[str]
) -> tuple[set[str], set[str]]:
    _validate_master_schema(master)
    nodes = master.get("nodes")
    edges = master.get("edges")
    if not isinstance(nodes, list) or not nodes:
        raise ValidationError("master.nodes: expected a non-empty list")
    if not isinstance(edges, list) or not edges:
        raise ValidationError("master.edges: expected a non-empty list")
    facts = evidence.get("facts") or {}

    for index, node in enumerate(nodes):
        location = f"master.nodes[{index}]"
        if not isinstance(node, dict):
            raise ValidationError(f"{location}: expected a mapping")
        _required_known_fields(
            node,
            NODE_FIELDS,
            NODE_FIELDS | NODE_OPTIONAL_FIELDS,
            location,
        )
        for field in ("id", "label", "domain", "gate", "presence", "lifecycle"):
            _nonempty_string(node[field], f"{location}.{field}")
        if node["presence"] not in NODE_PRESENCES:
            raise ValidationError(
                f"{location}.presence: unknown presence {node['presence']!r}"
            )
        if node["lifecycle"] not in LIFECYCLES:
            raise ValidationError(
                f"{location}.lifecycle: unknown lifecycle {node['lifecycle']!r}"
            )
        if node["as_of"] is not None and not isinstance(node["as_of"], date):
            raise ValidationError(f"{location}.as_of: expected a date or null")
        _string_list(node["source_ids"], f"{location}.source_ids")
        _string_list(node["fact_ids"], f"{location}.fact_ids")
        if "base_visible" in node and type(node["base_visible"]) is not bool:
            raise ValidationError(f"{location}.base_visible: expected a boolean")
        if "reveal_copy_ids" in node:
            _string_list(node["reveal_copy_ids"], f"{location}.reveal_copy_ids")

    for index, edge in enumerate(edges):
        location = f"master.edges[{index}]"
        if not isinstance(edge, dict):
            raise ValidationError(f"{location}: expected a mapping")
        _required_known_fields(
            edge,
            EDGE_FIELDS,
            EDGE_FIELDS | EDGE_OPTIONAL_FIELDS,
            location,
        )
        for field in (
            "id",
            "from",
            "to",
            "carries",
            "presence",
            "lifecycle",
            "normal_state",
            "flow_direction",
        ):
            _nonempty_string(edge[field], f"{location}.{field}")
        if edge["presence"] not in EDGE_PRESENCES:
            raise ValidationError(
                f"{location}.presence: unknown presence {edge['presence']!r}"
            )
        if edge["lifecycle"] not in LIFECYCLES:
            raise ValidationError(
                f"{location}.lifecycle: unknown lifecycle {edge['lifecycle']!r}"
            )
        if edge["normal_state"] not in EDGE_NORMAL_STATES:
            raise ValidationError(
                f"{location}.normal_state: unknown normal state "
                f"{edge['normal_state']!r}"
            )
        if edge["flow_direction"] not in EDGE_FLOW_DIRECTIONS:
            raise ValidationError(
                f"{location}.flow_direction: unknown flow direction "
                f"{edge['flow_direction']!r}"
            )
        _string_list(edge["source_ids"], f"{location}.source_ids")
        _string_list(edge["fact_ids"], f"{location}.fact_ids")
        if "base_visible" in edge and type(edge["base_visible"]) is not bool:
            raise ValidationError(f"{location}.base_visible: expected a boolean")
        if "reveal_copy_ids" in edge:
            _string_list(edge["reveal_copy_ids"], f"{location}.reveal_copy_ids")

    _validate_topology_presence_contract(nodes, edges)
    for index, node in enumerate(nodes):
        _validate_topology_posture(node, f"master.nodes[{index}]", kind="node")
    for index, edge in enumerate(edges):
        _validate_topology_posture(edge, f"master.edges[{index}]", kind="edge")

    node_ids = _unique((node["id"] for node in nodes), "master.nodes")
    edge_ids = _unique((edge["id"] for edge in edges), "master.edges")
    for node in nodes:
        _validate_fact_binding(node, facts, "node")
    for edge in edges:
        if edge["from"] not in node_ids or edge["to"] not in node_ids:
            raise ValidationError(
                f"edge {edge['id']}: endpoint absent from master nodes"
            )
        _validate_fact_binding(edge, facts, "edge")
    _source_refs(nodes, source_ids, "node")
    _source_refs(edges, source_ids, "edge")

    copy = master.get("copy")
    if not isinstance(copy, dict) or not copy:
        raise ValidationError("master.copy must be a non-empty mapping")
    copy_ids = set(copy)
    hidden_copy_ids = {
        copy_id
        for copy_id, spec in copy.items()
        if spec.get("base_visible", True) is False
    }
    owned_hidden_copy_ids: set[str] = set()
    for kind, records in (("node", nodes), ("edge", edges)):
        for record in records:
            location = f"{kind} {record['id']}.reveal_copy_ids"
            reveal_copy_ids = _string_list(record.get("reveal_copy_ids", []), location)
            if reveal_copy_ids and record.get("base_visible", True) is not False:
                raise ValidationError(
                    f"{kind} {record['id']}: only hidden records may own reveal copy"
                )
            unknown_copy_ids = reveal_copy_ids - copy_ids
            if unknown_copy_ids:
                raise ValidationError(
                    f"{kind} {record['id']}: unknown reveal copy IDs "
                    f"{sorted(unknown_copy_ids)}"
                )
            visible_copy_ids = reveal_copy_ids - hidden_copy_ids
            if visible_copy_ids:
                raise ValidationError(
                    f"{kind} {record['id']}: reveal copy must be base-hidden "
                    f"{sorted(visible_copy_ids)}"
                )
            owned_hidden_copy_ids.update(reveal_copy_ids)
    orphaned_hidden_copy_ids = hidden_copy_ids - owned_hidden_copy_ids
    if orphaned_hidden_copy_ids:
        raise ValidationError(
            "hidden master copy requires a hidden node/edge reveal owner: "
            f"{sorted(orphaned_hidden_copy_ids)}"
        )

    journeys = master["meta"]["journey_bar"]
    unknown_electrical = set(journeys["electrical"]) - set(tokens.VOLTAGE)
    unknown_thermal = set(journeys["thermal"]) - set(tokens.THERMAL)
    if unknown_electrical or unknown_thermal:
        raise ValidationError(
            f"journey token drift: electrical={sorted(unknown_electrical)} thermal={sorted(unknown_thermal)}"
        )

    node_map = {node["id"]: node for node in nodes}
    if node_map["bess_package"]["lifecycle"] != "future_design":
        raise ValidationError("BESS must remain future_design")
    if node_map["diesel_backup_package"]["lifecycle"] != "permitted":
        raise ValidationError("diesel backup must remain permitted, not operational")
    if "cooling_tower" in node_ids:
        raise ValidationError("Abilene base topology cannot contain a cooling tower")
    edge_map = {edge["id"]: edge for edge in edges}
    if edge_map["fill_to_facility_loop"]["to"] != "facility_loop":
        raise ValidationError("fill/treatment must connect to the closed facility loop")
    if edge_map["nuclear_ppa_overlay"]["carries"] != "contractual_attribute":
        raise ValidationError(
            "PPA must remain a contractual overlay, not a physical energy source"
        )

    serialised = str(master)
    for unsupported in ("20kV", "54VDC", "480 V", "345 kV -> 34.5 kV"):
        if unsupported in serialised:
            raise ValidationError(
                f"unsupported exact voltage leaked into master: {unsupported}"
            )
    return node_ids, edge_ids


def _validate_layout(
    master: dict[str, Any], layout: dict[str, Any], evidence: dict[str, Any]
) -> None:
    layout_pipeline._assert_coverage(master, layout)
    copy_ids = _copy_ids(layout)
    _unique(copy_ids, "rendered copy")
    for copy_id in copy_ids:
        layout_pipeline.resolve_copy(master, evidence, copy_id, include_hidden=True)
    hidden_copy_ids = {
        copy_id
        for copy_id, spec in master["copy"].items()
        if spec.get("base_visible", True) is False
    }
    missing_hidden_copy_ids = hidden_copy_ids - set(copy_ids)
    if missing_hidden_copy_ids:
        raise ValidationError(
            f"layout missing base-hidden master copy: {sorted(missing_hidden_copy_ids)}"
        )
    for section in ("zones", "regions", "labels", "room_labels"):
        for spec in layout.get(section) or []:
            forbidden = {"text", "title", "subtitle", "label"} & set(spec)
            if forbidden:
                raise ValidationError(
                    f"layout.{section}: semantic copy leaked into placement: {sorted(forbidden)}"
                )


def _validate_generated_svg(master: dict[str, Any], layout: dict[str, Any]) -> None:
    svg = (DIAGRAM / "master.svg").read_text()
    for node in master["nodes"]:
        if f'id="node-{node["id"]}"' not in svg:
            raise ValidationError(f"master.svg missing stable node ID {node['id']}")
    for edge in master["edges"]:
        if f'id="edge-{edge["id"]}"' not in svg:
            raise ValidationError(f"master.svg missing stable edge ID {edge['id']}")
    for copy_id in _copy_ids(layout):
        if f'id="label-{copy_id}"' not in svg:
            raise ValidationError(f"master.svg missing stable label ID {copy_id}")


def _validate_camera_assets(cameras: dict[str, Any]) -> None:
    for camera in cameras.get("cameras") or []:
        if asset := camera.get("map_asset"):
            path = DIAGRAM / asset
            if not path.exists():
                raise ValidationError(
                    f"camera {camera['id']}: missing generated map asset {asset}"
                )


def _claim_assertion_matches(assertion: str, fact: dict[str, Any]) -> bool:
    posture = fact["posture"]
    lifecycle = fact["lifecycle"]
    value = fact["value"]
    if assertion == "explicit_unknown":
        return (
            value is None
            and posture == "unverified_null"
            and lifecycle
            in {
                "as_built_unknown",
                "commissioning_unknown",
                "contract_term_unknown",
                "counterparty_unknown",
                "financing_terms_unknown",
                "installation_unknown",
                "operation_unknown",
                "ownership_unknown",
                "site_configuration_unknown",
                "topology_unknown",
            }
        )
    if assertion == "no_evidence_backed_estimate":
        return (
            value is None
            and posture == "no_evidence_backed_estimate"
            and lifecycle == "operation_unknown"
            and fact["basis"] == "no evidence-backed estimate"
        )
    if value is None:
        return False
    if assertion == "accounting_reference":
        return (
            lifecycle == "accounting_standard" and posture == "authoritative_guidance"
        )
    if assertion == "contract_reference":
        return (
            lifecycle
            in {
                "contracted",
                "contracted_structure",
                "operating_business_model",
            }
            and posture == "confirmed_contract"
        )
    if assertion == "reported_structure":
        return lifecycle == "announced_structure" and posture == "confirmed"
    if assertion == "business_model_reference":
        return lifecycle == "operating_business_model" and posture == "confirmed"
    if assertion == "method_reference":
        return (
            lifecycle
            in {
                "accounting_standard",
                "benchmark_method",
                "product_documented",
                "published_method",
            }
            and posture == "authoritative_guidance"
        )
    if assertion == "derived_scenario_reference":
        return (
            lifecycle == "derived_scenario_method"
            and posture == "derived_from_authoritative_sources"
        )
    if assertion == "confirmed":
        return (
            posture == "confirmed" and lifecycle in OPERATIONAL_ALLOWED_FACT_LIFECYCLES
        )
    if assertion == "confirmed_minimum":
        return (
            posture == "confirmed_minimum" and lifecycle in OPERATIONAL_FACT_LIFECYCLES
        )
    if assertion == "planned":
        return lifecycle == "planned" and posture == "planned_not_operational"
    if assertion == "permitted":
        return lifecycle == "permitted" and posture == "permitted_not_observed"
    if assertion == "future_design":
        return lifecycle == "future_design" and posture == "future_design"
    if assertion == "design_reference":
        return lifecycle in {"design_reference", "review_design"} and posture in {
            "design_not_as_built",
            "design_not_observed",
        }
    if assertion == "selected_design":
        return (
            lifecycle in {"design_requirement", "selected_design"}
            and posture == "design_selected"
        )
    if assertion == "product_reference":
        return lifecycle == "product_documented" and posture in {
            "confirmed_model_spec",
            "model_range_not_site_configured",
        }
    if assertion == "anticipated":
        return (
            lifecycle == "anticipated_maintenance"
            and posture == "anticipated_not_observed"
        )
    if assertion == "live_by":
        return lifecycle == "operating" and posture == "live_by_not_start_date"
    if assertion == "reported_untyped":
        return lifecycle == "delivered_untyped" and posture == "reported_untyped"
    if assertion == "excluded_scope":
        return lifecycle == "planned" and posture == "excluded_scope"
    return False


def _claim_payload_digest(claim: dict[str, Any]) -> str:
    return _contract_digest((claim["assertion"], claim["binding"], claim["fact_refs"]))


def _course_claim_contract_snapshot(
    course: dict[str, Any],
) -> dict[tuple[str, str], str]:
    snapshot: dict[tuple[str, str], str] = {}
    for act in course["acts"]:
        for segment in act["segments"]:
            for claim in segment["evidence"]["claims"]:
                key = (segment["id"], claim["id"])
                if key in snapshot:
                    raise ValidationError(
                        f"immutable course claim contract has duplicate key {key!r}"
                    )
                snapshot[key] = _claim_payload_digest(claim)
    return snapshot


def _validate_course_claim_contract(course: dict[str, Any]) -> None:
    actual = _course_claim_contract_snapshot(course)
    expected = dict(COURSE_CLAIM_CONTRACT)
    actual_keys = set(actual)
    expected_keys = set(expected)
    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys
    changed = sorted(
        key for key in actual_keys & expected_keys if actual[key] != expected[key]
    )
    if missing or extra or changed:
        raise ValidationError(
            "immutable course claim contract mismatch: "
            f"missing={sorted(missing)} extra={sorted(extra)} changed={changed}; "
            "assertion, binding, and ordered fact_refs require an explicit "
            "contract update"
        )


def _validate_course(
    course: dict[str, Any],
    master: dict[str, Any],
    evidence_ledgers: dict[str, dict[str, Any]],
    cameras: dict[str, Any],
) -> dict[str, int]:
    if type(course.get("schema_version")) is not int or course["schema_version"] != 2:
        raise ValidationError("course schema_version must be 2")
    if set(course) != {"schema_version", "meta", "acts"}:
        raise ValidationError(
            "course root must contain only schema_version, meta, and acts"
        )

    meta = course.get("meta")
    if not isinstance(meta, dict):
        raise ValidationError("course.meta: expected a mapping")
    _exact_fields(meta, COURSE_META_FIELDS, "course.meta")
    if meta["course_id"] != "gigawatt":
        raise ValidationError("course.meta.course_id must be gigawatt")
    if meta["inventory_scope"] != "complete_course":
        raise ValidationError("course inventory_scope must be complete_course")
    if meta["runtime_minutes"] is not None:
        raise ValidationError("course runtime remains unset until editorial review")
    for field, expected in (
        ("master", "diagram/master.yaml"),
        ("cameras", "diagram/cameras.yaml"),
    ):
        if meta[field] != expected:
            raise ValidationError(f"course.meta.{field} must reference {expected}")
    ledger_paths = _course_ledger_registry(meta)
    if set(evidence_ledgers) != set(ledger_paths):
        raise ValidationError(
            "course evidence ledger payloads must exactly match the registered ledger IDs"
        )
    _validate_registered_ledger_context_contract(evidence_ledgers)
    for ledger_id, ledger in evidence_ledgers.items():
        _validate_evidence_schema(
            ledger,
            f"evidence ledger {ledger_id}",
            ledger_id=ledger_id,
        )
    _validate_registered_fact_identity_contract(evidence_ledgers)
    master_ledger_id = meta["master_evidence_ledger"]
    if Path(master["meta"]["evidence_file"]) != ledger_paths[
        master_ledger_id
    ].relative_to(ROOT):
        raise ValidationError(
            "course master evidence ledger must point to master.meta.evidence_file"
        )
    _nonempty_string(meta["status"], "course.meta.status")
    _nonempty_string(meta["sequence_rule"], "course.meta.sequence_rule")
    relative_weight_total = meta["relative_weight_total"]
    if (
        isinstance(relative_weight_total, bool)
        or not isinstance(relative_weight_total, (int, float))
        or not math.isfinite(float(relative_weight_total))
    ):
        raise ValidationError(
            "course.meta.relative_weight_total must be finite numeric"
        )

    master_nodes = {node["id"]: node for node in master["nodes"]}
    master_edges = {edge["id"]: edge for edge in master["edges"]}
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    globally_bound_fact_refs = {
        f"{master_ledger_id}:{fact_id}"
        for record in [*master["nodes"], *master["edges"]]
        for fact_id in record.get("fact_ids") or []
    }

    acts = course.get("acts")
    if not isinstance(acts, list) or not acts:
        raise ValidationError("course.acts must be a non-empty list")
    act_ids: list[str] = []
    segment_ids: list[str] = []
    segments: list[dict[str, Any]] = []
    planned_shots: list[str] = []
    covered_nodes: set[str] = set()
    covered_edges: set[str] = set()
    total_weight = 0.0
    readiness_counts = {readiness: 0 for readiness in SEGMENT_READINESS}

    for act_index, act in enumerate(acts):
        location = f"course.acts[{act_index}]"
        if not isinstance(act, dict):
            raise ValidationError(f"{location}: expected a mapping")
        _exact_fields(act, ACT_FIELDS, location)
        _nonempty_string(act["id"], f"{location}.id")
        _nonempty_string(act["title"], f"{location}.title")
        _nonempty_string(act["learning_objective"], f"{location}.learning_objective")
        act_evidence_ledgers = _string_list(
            act["evidence_ledgers"],
            f"{location}.evidence_ledgers",
            allow_empty=False,
        )
        unknown_act_ledgers = act_evidence_ledgers - set(evidence_ledgers)
        if unknown_act_ledgers:
            raise ValidationError(
                f"act {act['id']}: unknown evidence ledgers {sorted(unknown_act_ledgers)}"
            )
        act_ids.append(act["id"])
        if not isinstance(act["segments"], list) or not act["segments"]:
            raise ValidationError(f"{location}.segments must be a non-empty list")

        for segment_index, segment in enumerate(act["segments"]):
            segment_location = f"{location}.segments[{segment_index}]"
            if not isinstance(segment, dict):
                raise ValidationError(f"{segment_location}: expected a mapping")
            _exact_fields(segment, SEGMENT_FIELDS, segment_location)
            for field in ("id", "title", "opening_question", "learning_objective"):
                _nonempty_string(segment[field], f"{segment_location}.{field}")
            segment_ids.append(segment["id"])
            segments.append(segment)

            weight = segment["weight"]
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
                or not math.isfinite(float(weight))
                or weight <= 0
            ):
                raise ValidationError(
                    f"{segment_location}.weight must be positive and finite"
                )
            total_weight += float(weight)
            _string_list(segment["depends_on"], f"{segment_location}.depends_on")

            camera = segment["camera"]
            if not isinstance(camera, dict):
                raise ValidationError(f"{segment_location}.camera: expected a mapping")
            _exact_fields(camera, SEGMENT_CAMERA_FIELDS, f"{segment_location}.camera")
            anchor_id = camera["anchor"]
            _nonempty_string(anchor_id, f"{segment_location}.camera.anchor")
            if anchor_id not in camera_map:
                raise ValidationError(
                    f"segment {segment['id']}: unknown camera anchor {anchor_id!r}"
                )
            _nonempty_string(camera["mode"], f"{segment_location}.camera.mode")
            if camera["mode"] not in scene_pipeline.ALLOWED_MODES:
                raise ValidationError(
                    f"segment {segment['id']}: invalid camera mode {camera['mode']!r}"
                )
            _nonempty_string(camera["status"], f"{segment_location}.camera.status")
            if camera["status"] not in SEGMENT_CAMERA_STATUS:
                raise ValidationError(
                    f"segment {segment['id']}: invalid camera status {camera['status']!r}"
                )
            _nonempty_string(camera["shot"], f"{segment_location}.camera.shot")
            reveal_ids = _string_list(
                camera["reveal_ids"], f"{segment_location}.camera.reveal_ids"
            )
            reveal_copy_ids = _string_list(
                camera["reveal_copy_ids"],
                f"{segment_location}.camera.reveal_copy_ids",
            )

            node_ids = segment["node_ids"]
            edge_ids = segment["edge_ids"]
            selected_nodes = _string_list(
                node_ids,
                f"segment {segment['id']}.node_ids",
                allow_empty=False,
            )
            selected_edges = _string_list(
                edge_ids,
                f"segment {segment['id']}.edge_ids",
            )
            unknown_nodes = selected_nodes - set(master_nodes)
            unknown_edges = selected_edges - set(master_edges)
            if unknown_nodes or unknown_edges:
                raise ValidationError(
                    f"segment {segment['id']}: unknown_nodes={sorted(unknown_nodes)} "
                    f"unknown_edges={sorted(unknown_edges)}"
                )
            incomplete_edges = sorted(
                edge_id
                for edge_id in selected_edges
                if {
                    master_edges[edge_id]["from"],
                    master_edges[edge_id]["to"],
                }
                - selected_nodes
            )
            if incomplete_edges:
                raise ValidationError(
                    f"segment {segment['id']}: edge endpoints absent for {incomplete_edges}"
                )

            hidden_selected = {
                node_id
                for node_id in selected_nodes
                if master_nodes[node_id].get("base_visible", True) is False
            } | {
                edge_id
                for edge_id in selected_edges
                if master_edges[edge_id].get("base_visible", True) is False
            }
            hidden_selected_records = [
                master_nodes[node_id]
                for node_id in selected_nodes
                if node_id in hidden_selected
            ] + [
                master_edges[edge_id]
                for edge_id in selected_edges
                if edge_id in hidden_selected
            ]
            expected_reveal_copy_ids = {
                copy_id
                for record in hidden_selected_records
                for copy_id in record.get("reveal_copy_ids", [])
            }

            if camera["status"] == "existing":
                if reveal_ids or reveal_copy_ids:
                    raise ValidationError(
                        f"segment {segment['id']}: existing camera cannot request hidden reveals"
                    )
                anchor = camera_map[anchor_id]
                if camera["shot"] != anchor_id or camera["mode"] != anchor["mode"]:
                    raise ValidationError(
                        f"segment {segment['id']}: existing shot must equal its anchor and mode"
                    )
                anchor_nodes = set(anchor.get("focus_nodes") or [])
                anchor_edges = set(anchor.get("focus_edges") or [])
                if (anchor_nodes and not selected_nodes <= anchor_nodes) or (
                    anchor_edges and not selected_edges <= anchor_edges
                ):
                    raise ValidationError(
                        f"segment {segment['id']}: focus exceeds existing camera {anchor_id}"
                    )
                if hidden_selected:
                    raise ValidationError(
                        f"segment {segment['id']}: existing camera cannot reveal hidden "
                        f"IDs={sorted(hidden_selected)}"
                    )
            else:
                if camera["shot"] == anchor_id:
                    raise ValidationError(
                        f"segment {segment['id']}: planned shot must have a new shot ID"
                    )
                if reveal_ids != hidden_selected:
                    raise ValidationError(
                        f"segment {segment['id']}: planned reveal_ids must exactly match "
                        f"selected hidden IDs {sorted(hidden_selected)}"
                    )
                if reveal_copy_ids != expected_reveal_copy_ids:
                    raise ValidationError(
                        f"segment {segment['id']}: planned reveal_copy_ids must exactly "
                        "match selected hidden copy IDs "
                        f"{sorted(expected_reveal_copy_ids)}"
                    )
                planned_shots.append(camera["shot"])

            segment_evidence = segment["evidence"]
            if not isinstance(segment_evidence, dict):
                raise ValidationError(
                    f"{segment_location}.evidence: expected a mapping"
                )
            _exact_fields(
                segment_evidence,
                SEGMENT_EVIDENCE_FIELDS,
                f"{segment_location}.evidence",
            )
            readiness = segment_evidence["readiness"]
            _nonempty_string(readiness, f"{segment_location}.evidence.readiness")
            if readiness not in SEGMENT_READINESS:
                raise ValidationError(
                    f"segment {segment['id']}: invalid readiness {readiness!r}"
                )
            readiness_counts[readiness] += 1

            claims = segment_evidence["claims"]
            blockers = segment_evidence["blocking_research"]
            guards = segment_evidence["promotion_guards"]
            if not isinstance(claims, list):
                raise ValidationError(f"segment {segment['id']}: claims must be a list")
            if not isinstance(blockers, list) or any(
                not isinstance(item, str) or not item.strip() for item in blockers
            ):
                raise ValidationError(
                    f"segment {segment['id']}: blocking_research must be a string list"
                )
            invalid_blockers = [
                item
                for item in blockers
                if len(item.strip()) < 20
                or item.strip().casefold().rstrip(".?!") in BLOCKER_PLACEHOLDERS
                or item.strip()[-1] not in ".?!"
            ]
            if invalid_blockers:
                raise ValidationError(
                    f"segment {segment['id']}: blocking_research contains placeholders "
                    f"or underspecified items {invalid_blockers}"
                )
            guard_set = _string_list(
                guards,
                f"segment {segment['id']}.promotion_guards",
                allow_empty=False,
            )
            unknown_guards = guard_set - PROMOTION_GUARDS
            if unknown_guards:
                raise ValidationError(
                    f"segment {segment['id']}: unknown promotion guards {sorted(unknown_guards)}"
                )
            if readiness == "evidence_ready" and (blockers or not claims):
                raise ValidationError(
                    f"segment {segment['id']}: evidence_ready requires claims and no blockers"
                )
            if readiness == "research_required" and not blockers:
                raise ValidationError(
                    f"segment {segment['id']}: research_required needs blocking research"
                )

            selected_fact_refs = {
                f"{master_ledger_id}:{fact_id}"
                for record_id in selected_nodes
                for fact_id in master_nodes[record_id].get("fact_ids") or []
            } | {
                f"{master_ledger_id}:{fact_id}"
                for record_id in selected_edges
                for fact_id in master_edges[record_id].get("fact_ids") or []
            }
            claim_ids: list[str] = []
            claimed_fact_refs: list[str] = []
            required_guards: set[str] = set()
            for claim_index, claim in enumerate(claims):
                claim_location = f"{segment_location}.evidence.claims[{claim_index}]"
                if not isinstance(claim, dict):
                    raise ValidationError(f"{claim_location}: expected a mapping")
                _exact_fields(claim, SEGMENT_CLAIM_FIELDS, claim_location)
                _nonempty_string(claim["id"], f"{claim_location}.id")
                claim_ids.append(claim["id"])
                assertion = claim["assertion"]
                _nonempty_string(assertion, f"{claim_location}.assertion")
                if assertion not in SEGMENT_ASSERTIONS:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: invalid assertion {assertion!r}"
                    )
                binding = claim["binding"]
                _nonempty_string(binding, f"{claim_location}.binding")
                if binding not in SEGMENT_CLAIM_BINDINGS:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: invalid binding {binding!r}"
                    )
                fact_refs = claim["fact_refs"]
                _string_list(
                    fact_refs,
                    f"{claim_location}.fact_refs",
                    allow_empty=False,
                )
                claimed_fact_refs.extend(fact_refs)
                resolved = [
                    _resolve_fact_ref(fact_ref, evidence_ledgers, claim_location)
                    for fact_ref in fact_refs
                ]
                out_of_scope_ledgers = sorted(
                    {
                        ledger_id
                        for ledger_id, _, _ in resolved
                        if ledger_id not in act_evidence_ledgers
                    }
                )
                if out_of_scope_ledgers:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: evidence ledgers "
                        f"outside act scope {out_of_scope_ledgers}"
                    )
                if binding == "topology":
                    misplaced = sorted(set(fact_refs) - selected_fact_refs)
                    if misplaced:
                        raise ValidationError(
                            f"segment {segment['id']} claim {claim['id']}: topology facts "
                            f"are not bound to selected topology {misplaced}"
                        )
                else:
                    master_bound = sorted(set(fact_refs) & globally_bound_fact_refs)
                    if master_bound:
                        raise ValidationError(
                            f"segment {segment['id']} claim {claim['id']}: overlay cannot "
                            f"bypass master topology binding {master_bound}"
                        )
                    if any(
                        ledger_id != master_ledger_id for ledger_id, _, _ in resolved
                    ) and ("site_scope_transfer" not in guard_set):
                        raise ValidationError(
                            f"segment {segment['id']} claim {claim['id']}: external-ledger "
                            "overlay requires site_scope_transfer"
                        )

                incompatible = sorted(
                    fact_ref
                    for fact_ref, (_, _, fact) in zip(fact_refs, resolved)
                    if not _claim_assertion_matches(assertion, fact)
                )
                if incompatible:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: facts {incompatible} "
                        f"cannot support assertion {assertion!r}"
                    )

                numeric_scopes_by_unit: dict[str, set[str]] = {}
                for _, _, fact in resolved:
                    value = fact["value"]
                    unit = fact["unit"]
                    if (
                        isinstance(value, (int, float))
                        and not isinstance(value, bool)
                        and unit
                    ):
                        numeric_scopes_by_unit.setdefault(str(unit), set()).add(
                            fact["scope"]
                        )
                additive_scope_collisions = {
                    unit: scopes
                    for unit, scopes in numeric_scopes_by_unit.items()
                    if len(scopes) > 1
                }
                if additive_scope_collisions:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: one claim cannot "
                        f"combine same-unit numeric facts across scopes {additive_scope_collisions}"
                    )
                required_guards.update(ASSERTION_REQUIRED_GUARDS.get(assertion, set()))
            _unique(claim_ids, f"segment {segment['id']}.claim IDs")
            _unique(
                claimed_fact_refs, f"segment {segment['id']}.claimed fact references"
            )
            missing_guards = required_guards - guard_set
            if missing_guards:
                raise ValidationError(
                    f"segment {segment['id']}: missing assertion promotion guards "
                    f"{sorted(missing_guards)}"
                )

            covered_nodes.update(selected_nodes)
            covered_edges.update(selected_edges)

    _unique(act_ids, "course act IDs")
    _unique(segment_ids, "course segment IDs")
    _unique(planned_shots, "course planned shot IDs")
    segment_index = {segment_id: index for index, segment_id in enumerate(segment_ids)}
    segment_readiness = {
        segment["id"]: segment["evidence"]["readiness"] for segment in segments
    }
    for index, segment in enumerate(segments):
        dependencies = set(segment["depends_on"])
        unavailable = sorted(
            dependency
            for dependency in dependencies
            if dependency not in segment_index or segment_index[dependency] >= index
        )
        if unavailable:
            raise ValidationError(
                f"segment {segment['id']}: dependencies must name earlier segments {unavailable}"
            )
        gated_dependencies = sorted(
            dependency
            for dependency in dependencies
            if segment_readiness[dependency] != "evidence_ready"
        )
        if segment_readiness[segment["id"]] == "evidence_ready" and gated_dependencies:
            raise ValidationError(
                f"segment {segment['id']}: evidence_ready cannot depend on research-gated "
                f"segments {gated_dependencies}"
            )
    shot_collisions = sorted(set(planned_shots) & set(camera_map))
    if shot_collisions:
        raise ValidationError(
            f"course planned shot IDs collide with existing cameras: {shot_collisions}"
        )
    if not math.isclose(
        total_weight,
        float(meta["relative_weight_total"]),
        rel_tol=0.0,
        abs_tol=1e-9,
    ):
        raise ValidationError(
            f"course relative weight mismatch: declared {meta['relative_weight_total']}, "
            f"computed {total_weight}"
        )

    for index, segment in enumerate(segments):
        transition = segment["transition"]
        if index == len(segments) - 1:
            if transition is not None:
                raise ValidationError("final course segment transition must be null")
            continue
        if not isinstance(transition, dict):
            raise ValidationError(
                f"segment {segment['id']}: transition must be a mapping"
            )
        _exact_fields(
            transition, SEGMENT_TRANSITION_FIELDS, f"segment {segment['id']}.transition"
        )
        _nonempty_string(transition["cue"], f"segment {segment['id']}.transition.cue")
        expected = segments[index + 1]["id"]
        if transition["to"] != expected:
            raise ValidationError(
                f"segment {segment['id']}: transition must target next segment {expected!r}"
            )

    visible_nodes = {
        node_id
        for node_id, node in master_nodes.items()
        if node.get("base_visible", True) is not False
    }
    visible_edges = {
        edge_id
        for edge_id, edge in master_edges.items()
        if edge.get("base_visible", True) is not False
    }
    missing_nodes = sorted(visible_nodes - covered_nodes)
    missing_edges = sorted(visible_edges - covered_edges)
    if missing_nodes or missing_edges:
        raise ValidationError(
            "complete course coverage mismatch: "
            f"missing_nodes={missing_nodes} missing_edges={missing_edges}"
        )

    _validate_course_claim_contract(course)

    return {
        "acts": len(acts),
        "segments": len(segments),
        "evidence_ready_segments": readiness_counts["evidence_ready"],
        "research_required_segments": readiness_counts["research_required"],
        "planned_shots": len(planned_shots),
    }


def validate_course_inputs(
    course: dict[str, Any],
    master: dict[str, Any],
    evidence_ledgers: dict[str, dict[str, Any]],
    cameras: dict[str, Any],
) -> dict[str, int]:
    """Run the authoritative evidence and course contract before compilation."""
    return _validate_course(course, master, evidence_ledgers, cameras)


def validate_project() -> dict[str, Any]:
    master = _load_yaml_strict(DIAGRAM / "master.yaml")
    layout = _load_yaml_strict(DIAGRAM / "layout.yaml")
    evidence = _load_yaml_strict(EVIDENCE)
    scene = _load_yaml_strict(DIAGRAM / "scene.yaml")
    cameras = _load_yaml_strict(DIAGRAM / "cameras.yaml")
    course = _load_yaml_strict(COURSE)
    course_visuals = _load_yaml_strict(COURSE_VISUALS)
    course_ledgers = _load_course_evidence_ledgers(course)

    source_ids, _ = _validate_evidence(evidence)
    node_ids, edge_ids = _validate_master(master, evidence, source_ids)
    _validate_layout(master, layout, evidence)
    scene_pipeline.validate(master, scene, cameras)
    _validate_generated_svg(master, layout)
    _validate_camera_assets(cameras)
    course_result = _validate_course(course, master, course_ledgers, cameras)
    course_runtime_pipeline._compiled_visuals(course, cameras, master, course_visuals)
    try:
        generated_artifacts = generated_artifacts_pipeline.build_expected_artifacts(
            master,
            layout,
            evidence,
            cameras,
        )
        generated_artifacts_pipeline.assert_current(generated_artifacts)
    except generated_artifacts_pipeline.GeneratedArtifactError as error:
        raise ValidationError(str(error)) from error

    registered_source_count = sum(
        len(ledger.get("sources") or {}) for ledger in course_ledgers.values()
    )
    registered_fact_count = sum(
        len(ledger.get("facts") or {}) for ledger in course_ledgers.values()
    )

    html, digest = scene_pipeline.generate()
    if html != (DIAGRAM / "hybrid.html").read_text():
        raise ValidationError("hybrid.html is stale; run gigawatt-scene")
    shot_registry, shot_review, shot_digest = shots_pipeline.build_artifacts()
    if shot_registry != shots_pipeline.REGISTRY_PATH.read_text():
        raise ValidationError("planned_shots.json is stale; run gigawatt-shots")
    if shot_review != shots_pipeline.REVIEW_PATH.read_text():
        raise ValidationError("planned_shots.html is stale; run gigawatt-shots")
    course_registry, course_player, instructor_packet, course_digest = (
        course_runtime_pipeline.build_artifacts()
    )
    if course_registry != course_runtime_pipeline.REGISTRY_PATH.read_text():
        raise ValidationError("course_runtime.json is stale; run gigawatt-course")
    if course_player != course_runtime_pipeline.PLAYER_PATH.read_text():
        raise ValidationError("course.html is stale; run gigawatt-course")
    if instructor_packet != course_runtime_pipeline.PACKET_PATH.read_text():
        raise ValidationError("INSTRUCTOR_PACKET.md is stale; run gigawatt-course")
    quality_registry, dependency_graph, quality_digest = (
        quality_pipeline.build_artifacts()
    )
    if quality_registry.encode() != quality_pipeline.QUALITY_PATH.read_bytes():
        raise ValidationError("course_quality.json is stale; run gigawatt-quality")
    if dependency_graph.encode() != quality_pipeline.GRAPH_PATH.read_bytes():
        raise ValidationError(
            "course_dependency_graph.json is stale; run gigawatt-quality"
        )
    return {
        "evidence_ledgers": len(course_ledgers),
        "sources": registered_source_count,
        "facts": registered_fact_count,
        "nodes": len(node_ids),
        "edges": len(edge_ids),
        "cameras": len(cameras["cameras"]),
        "verified_generated_artifacts": len(generated_artifacts),
        "hybrid_digest": digest,
        "planned_shots_digest": shot_digest,
        "course_runtime_digest": course_digest,
        "quality_digest": quality_digest,
        **course_result,
    }


def main() -> None:
    result = validate_project()
    print(
        "validated "
        f"{result['evidence_ledgers']} evidence ledgers · "
        f"{result['sources']} sources · {result['facts']} facts · "
        f"{result['nodes']} nodes · {result['edges']} edges · "
        f"{result['cameras']} cameras · {result['acts']} acts · "
        f"{result['segments']} segments "
        f"({result['evidence_ready_segments']} evidence-ready / "
        f"{result['research_required_segments']} research-gated) · "
        f"{result['planned_shots']} planned shots · hybrid {result['hybrid_digest']}"
    )


if __name__ == "__main__":
    main()
