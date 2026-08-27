from __future__ import annotations

import json
import math
import unittest

from gigawatt import course_runtime, shots, validate


def walk_keys(value: object):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            yield from walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_keys(nested)


class CourseRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        (
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
            cls.ledgers,
        ) = course_runtime.load_inputs()
        cls.registry = course_runtime.compile_registry(
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
            cls.ledgers,
            source_digest="test-digest",
        )

    def test_registry_covers_the_canonical_course_exactly(self) -> None:
        manifest_segments = [
            segment for act in self.course["acts"] for segment in act["segments"]
        ]
        runtime_segments = self.registry["segments"]
        self.assertEqual(7, self.registry["act_count"])
        self.assertEqual(26, self.registry["segment_count"])
        self.assertEqual(
            [segment["id"] for segment in manifest_segments],
            [segment["segment_id"] for segment in runtime_segments],
        )
        self.assertEqual(
            list(range(1, 27)), [segment["sequence"] for segment in runtime_segments]
        )
        self.assertEqual(
            {"derived": 21, "existing": 5},
            {
                status: sum(segment["status"] == status for segment in runtime_segments)
                for status in ("derived", "existing")
            },
        )
        self.assertEqual(
            sum(
                segment["evidence"]["readiness"] == "evidence_ready"
                for segment in manifest_segments
            ),
            self.registry["evidence_ready_count"],
        )
        self.assertEqual(
            validate.PROMOTION_GUARDS,
            set(course_runtime.PROMOTION_GUARD_WARNINGS),
        )
        self.assertTrue(
            all(
                segment["promotion_guard_warnings"]
                for segment in self.registry["segments"]
            )
        )

    def test_runtime_contains_no_pacing_or_spoken_script_contract(self) -> None:
        forbidden = course_runtime.FORBIDDEN_RUNTIME_KEYS
        self.assertFalse(
            forbidden & {key.casefold() for key in walk_keys(self.registry)}
        )

    def test_planned_frames_match_the_planned_shot_compiler(self) -> None:
        planned = shots.compile_registry(
            self.course,
            self.cameras,
            self.master,
            self.layout,
            self.scene,
            source_digest="test-digest",
        )
        planned_by_segment = {shot["segment_id"]: shot for shot in planned["shots"]}
        for segment in self.registry["segments"]:
            if segment["status"] == "derived":
                self.assertEqual(
                    planned_by_segment[segment["segment_id"]]["frame"],
                    segment["frame"],
                )

    def test_every_frame_is_finite_and_every_claim_is_resolved(self) -> None:
        for segment in self.registry["segments"]:
            frame = segment["frame"]
            geometry = (
                [*frame["viewBox"], *frame["anchor_viewBox"]]
                if frame["kind"] == "2d"
                else [
                    *frame["position"],
                    *frame["target"],
                    *frame["anchor_position"],
                    *frame["anchor_target"],
                ]
            )
            self.assertTrue(all(math.isfinite(float(value)) for value in geometry))
            self.assertTrue(segment["claims"] or segment["blocking_research"])
            for claim in segment["claims"]:
                self.assertTrue(claim["facts"])
                for fact in claim["facts"]:
                    self.assertTrue(fact["value"])
                    self.assertTrue(fact["scope"])
                    self.assertTrue(fact["sources"])
                    self.assertTrue(
                        all(
                            source["url"].startswith("https://")
                            for source in fact["sources"]
                        )
                    )

    def test_generated_player_and_packet_are_current_and_manual(self) -> None:
        registry_json, player, packet, digest = course_runtime.build_artifacts()
        second_registry, second_player, second_packet, second_digest = (
            course_runtime.build_artifacts()
        )
        self.assertEqual(
            (registry_json, player, packet, digest),
            (second_registry, second_player, second_packet, second_digest),
        )
        self.assertEqual(registry_json, course_runtime.REGISTRY_PATH.read_text())
        self.assertEqual(player, course_runtime.PLAYER_PATH.read_text())
        self.assertEqual(packet, course_runtime.PACKET_PATH.read_text())
        self.assertEqual(digest, json.loads(registry_json)["source_digest"])
        self.assertIn('id="previous"', player)
        self.assertIn('id="next"', player)
        self.assertNotIn('id="context-toggle"', player)
        self.assertNotIn('$("context-toggle").addEventListener', player)
        self.assertIn('id="evidence-toggle"', player)
        self.assertIn('id="notes-panel"', player)
        self.assertIn('aria-controls="notes-panel"', player)
        self.assertIn('aria-expanded="false"', player)
        self.assertIn('aria-hidden="true" inert', player)
        self.assertIn('aria-label="Course navigation and evidence controls"', player)
        self.assertIn("panel.inert = !open", player)
        self.assertIn('$("notes-panel").scrollTop = 0', player)
        self.assertIn(
            'const restorePanelFocus = notesOpen && $("notes-panel").contains(document.activeElement);',
            player,
        )
        self.assertIn('if (restorePanelFocus) $("notes-close").focus();', player)
        self.assertIn("#three-mount .node-label small { display: none; }", player)
        self.assertIn(
            '#three-mount .node-label[data-presence="teaching_reference"]', player
        )
        self.assertIn('notesSection("What the evidence supports")', player)
        self.assertIn('"Evidence ready"', player)
        self.assertIn('"supported claim group"', player)
        self.assertIn(
            "const knownLimitCount = knownLimits.reduce(",
            player,
        )
        self.assertIn("notesDisclosure(`Known limits (${knownLimitCount})`", player)
        self.assertIn(
            "notesDisclosure(`Avoid overclaiming (${shot.promotion_guard_warnings.length})`",
            player,
        )
        self.assertIn(
            'new Set(["explicit_unknown", "no_evidence_backed_estimate"])', player
        )
        self.assertLess(
            player.index('notesSection("What the evidence supports")'),
            player.index("notesDisclosure(`Avoid overclaiming"),
        )
        self.assertLess(
            player.index("if (shot.blocking_research.length)"),
            player.index('notesSection("What the evidence supports")'),
        )
        self.assertNotIn('notesSection("Teaching territory")', player)
        self.assertIn('event.key === "ArrowLeft"', player)
        self.assertIn('event.key === "ArrowRight"', player)
        self.assertNotIn("setTimeout(", player)
        self.assertNotIn("setInterval(", player)
        self.assertNotIn("requestAnimationFrame(", player)
        self.assertIn("not a spoken script", packet.casefold())
        self.assertIn("Red-line warnings:", packet)
        self.assertIn("scenario to site estimate", packet.casefold())

    def test_embedded_json_is_script_safe(self) -> None:
        encoded = course_runtime._script_safe_payload({"title": "x</script>y"})
        self.assertNotIn("</script>", encoded)
        self.assertIn("<\\/script>", encoded)

    def test_semantic_units_are_qualified_not_concatenated(self) -> None:
        self.assertEqual(
            "A reserved slot can precede readiness (project-delivery relationship)",
            course_runtime._display_value(
                {
                    "value": "A reserved slot can precede readiness",
                    "unit": "project-delivery relationship",
                }
            ),
        )
        self.assertEqual(
            "36 months",
            course_runtime._display_value({"value": 36, "unit": "months"}),
        )

    def test_final_segment_has_a_close_not_an_invented_next_segment(self) -> None:
        self.assertIsNone(self.registry["segments"][-1]["transition"])
        self.assertIn("Close:", course_runtime.PACKET_PATH.read_text())


if __name__ == "__main__":
    unittest.main()
