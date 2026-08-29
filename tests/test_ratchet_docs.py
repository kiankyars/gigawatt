import json
import unittest
from pathlib import Path

from gigawatt import quality

ROOT = Path(__file__).resolve().parents[1]
FROZEN_SHA = "0856a93b78181bec3945168632d141595575800c"


class RatchetDocumentationTests(unittest.TestCase):
    def test_documented_statuses_and_gates_match_compiled_ratchet(self) -> None:
        manifest = quality.load_ratchet_manifest()
        registry = json.loads((ROOT / "diagram" / "course_quality.json").read_text())
        ratchet = registry["ratchet"]
        self.assertEqual(ratchet["acceptance"], manifest["acceptance"])

        challengers = ratchet["challengers"]
        self.assertEqual(
            [challenger["id"] for challenger in challengers],
            ["labels_only", "annotations_only", "combined"],
        )
        self.assertEqual(
            ratchet["frozen_champion_metadata"]["git_sha"], FROZEN_SHA
        )
        self.assertEqual(
            {
                challenger["id"]: (
                    challenger["modeled_gate_status"],
                    challenger["pareto_disposition"],
                    challenger["final_acceptance"],
                    challenger["final_acceptance_evaluation"][
                        "promotion_eligible"
                    ],
                )
                for challenger in challengers
            },
            {
                "labels_only": ("pending", "pending", "pending", False),
                "annotations_only": ("failed", "rejected", "rejected", False),
                "combined": ("pending", "pending", "pending", False),
            },
        )
        combined = challengers[-1]
        self.assertEqual(
            combined["visual_sources"],
            {"annotation_source": "current", "label_source": "current"},
        )

        gate_ids = tuple(quality.FINAL_ACCEPTANCE_GATE_IDS)
        self.assertEqual(len(gate_ids), 5)
        acceptance_by_candidate = {
            record["candidate_id"]: record
            for record in ratchet["acceptance"]["candidates"]
        }
        self.assertEqual(
            list(acceptance_by_candidate), [item["id"] for item in challengers]
        )
        for challenger in challengers:
            candidate_id = challenger["id"]
            candidate_input = acceptance_by_candidate[candidate_id]
            final_evaluation = challenger["final_acceptance_evaluation"]
            self.assertEqual(
                final_evaluation["candidate_provenance_sha256"],
                candidate_input["candidate_provenance_sha256"],
            )
            self.assertEqual(
                tuple(final_evaluation["required_gate_ids"]),
                gate_ids,
            )
            self.assertEqual(
                set(final_evaluation["gate_evidence"]),
                set(gate_ids),
            )
            self.assertEqual(final_evaluation["manifest_gate_status"], "pending")
            self.assertEqual(final_evaluation["evidence_final_status"], "pending")
            self.assertTrue(
                all(
                    gate["status"] == "pending"
                    and gate["evidence_ref"] is None
                    and gate["evidence"] is None
                    for gate in final_evaluation["gate_evidence"].values()
                )
            )

        status_text = (
            "Current compiled challenger statuses "
            "(`diagram/course_quality.json`): "
            + "; ".join(
                f"`{challenger['id']}` modeled "
                f"`{challenger['modeled_gate_status']}`, Pareto "
                f"`{challenger['pareto_disposition']}`, final "
                f"`{challenger['final_acceptance']}`"
                for challenger in challengers
            )
            + "."
        )
        gate_text = (
            "Required final-acceptance gate IDs: "
            + ", ".join(f"`{gate_id}`" for gate_id in gate_ids)
            + "."
        )

        root_readme = (ROOT / "README.md").read_text()
        course_readme = (ROOT / "course" / "README.md").read_text()
        redline = (ROOT / "course" / "REDLINE.md").read_text()
        for document in (root_readme, course_readme, redline):
            normalized = " ".join(document.split())
            self.assertIn(FROZEN_SHA, normalized)
            self.assertIn("No working-tree variant is accepted.", normalized)
            self.assertIn(status_text, normalized)
            self.assertIn(
                "The `combined` challenger is the current rendered runtime.",
                normalized,
            )
            self.assertIn(
                "Final acceptance is separate from modeled/Pareto evaluation.",
                normalized,
            )
            self.assertIn(gate_text, normalized)
            self.assertIn(
                "The blind-review gate requires two of three reviewer preferences.",
                normalized,
            )
            self.assertIn(
                "remain preserved in the frozen commit and its Git ancestry",
                normalized,
            )

        self.assertIn("That historical result is not browser evidence", course_readme)
        self.assertIn("frozen champion only", redline)
        self.assertNotIn(
            "The package is ready for an instructor walkthrough",
            redline,
        )


if __name__ == "__main__":
    unittest.main()
