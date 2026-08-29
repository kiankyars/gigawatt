import copy
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from gigawatt import champion, quality


class FrozenChampionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = quality.load_ratchet_manifest()

    def test_frozen_champion_is_reconstructed_from_git_objects(self) -> None:
        result = champion.require_frozen_champion(self.manifest["frozen_champion"])
        self.assertTrue(result["static_integrity_passed"])
        self.assertEqual(result["failures"], [])
        self.assertEqual(
            result["missing_live_evidence"],
            [
                "historical_per_viewport_frame_captures",
                "historical_per_viewport_quality_vectors",
            ],
        )
        self.assertEqual(
            result["historical_test_reproduction"]["expected_test_count"], 349
        )
        self.assertEqual(
            result["historical_test_reproduction"]["status"],
            "requires_external_execution",
        )
        provenance = result["provenance_state"]
        self.assertEqual(
            provenance["origin_main_tracking_ref"]["observation_kind"],
            "local_remote_tracking_ref",
        )
        self.assertFalse(provenance["origin_main_tracking_ref"]["integrity_relevant"])
        self.assertEqual(provenance["live_remote"]["status"], "not_checked")

    def test_tree_aggregate_matches_the_frozen_manifest(self) -> None:
        frozen = self.manifest["frozen_champion"]
        self.assertEqual(
            champion.tree_aggregate_sha256(champion.ROOT, frozen["git_sha"]),
            frozen["source_tree_aggregate_sha256"],
        )

    def test_changed_worktree_paths_include_untracked_and_survive_a_commit(
        self,
    ) -> None:
        with TemporaryDirectory() as temporary_directory:
            repo = Path(temporary_directory)
            champion._git(repo, "init", "--quiet")
            champion._git(repo, "config", "user.name", "Quality Test")
            champion._git(repo, "config", "user.email", "quality@example.invalid")
            tracked_path = repo / "tracked.txt"
            tracked_path.write_text("frozen\n")
            champion._git(repo, "add", "--", tracked_path.name)
            champion._git(repo, "commit", "--quiet", "-m", "frozen")
            frozen_sha = champion._git(repo, "rev-parse", "HEAD").decode().strip()

            tracked_path.write_text("changed\n")
            (repo / "untracked.txt").write_text("new\n")
            before_commit = champion.changed_worktree_paths(repo, frozen_sha)
            self.assertEqual(before_commit, ("tracked.txt", "untracked.txt"))

            champion._git(repo, "add", "--all")
            champion._git(repo, "commit", "--quiet", "-m", "later")
            self.assertEqual(
                champion.changed_worktree_paths(repo, frozen_sha),
                before_commit,
            )

    def test_mutated_champion_hash_fails_closed(self) -> None:
        broken = copy.deepcopy(self.manifest["frozen_champion"])
        broken["artifact_sha256"]["diagram/course.html"] = "0" * 64
        result = champion.verify_frozen_champion(broken)
        self.assertFalse(result["static_integrity_passed"])
        self.assertEqual(
            [failure["id"] for failure in result["failures"]],
            ["artifact:diagram/course.html"],
        )
        with self.assertRaisesRegex(
            champion.ChampionVerificationError,
            "artifact:diagram/course.html",
        ):
            champion.require_frozen_champion(broken)

    def test_unknown_champion_field_fails_closed(self) -> None:
        broken = copy.deepcopy(self.manifest["frozen_champion"])
        broken["unknown_live_approval"] = True

        with self.assertRaises(champion.ChampionVerificationError) as raised:
            champion.verify_frozen_champion(broken)

        self.assertEqual(
            str(raised.exception),
            "champion fields must be exact; "
            "missing=[] unknown=['unknown_live_approval']",
        )

    def test_missing_and_unknown_champion_fields_fail_together(self) -> None:
        broken = copy.deepcopy(self.manifest["frozen_champion"])
        del broken["origin_sha"]
        broken["replacement_origin"] = "f" * 40

        with self.assertRaises(champion.ChampionVerificationError) as raised:
            champion.verify_frozen_champion(broken)

        self.assertEqual(
            str(raised.exception),
            "champion fields must be exact; "
            "missing=['origin_sha'] unknown=['replacement_origin']",
        )

    def test_nested_champion_scalar_types_and_full_digests_fail_closed(self) -> None:
        artifact_name = next(iter(self.manifest["frozen_champion"]["artifact_sha256"]))
        mutations = (
            (
                "git sha boolean",
                lambda record: record.__setitem__("git_sha", True),
                "champion.git_sha",
            ),
            (
                "origin sha integer",
                lambda record: record.__setitem__("origin_sha", 0),
                "champion.origin_sha",
            ),
            (
                "short tree digest",
                lambda record: record.__setitem__(
                    "source_tree_aggregate_sha256", "0" * 63
                ),
                "source_tree_aggregate_sha256",
            ),
            (
                "nonhex runtime digest",
                lambda record: record.__setitem__(
                    "baseline_runtime_source_digest", "z" * 64
                ),
                "baseline_runtime_source_digest",
            ),
            (
                "floating test count",
                lambda record: record.__setitem__("baseline_test_count", 349.0),
                "positive integer",
            ),
            (
                "boolean test count",
                lambda record: record.__setitem__("baseline_test_count", True),
                "positive integer",
            ),
            (
                "artifact sequence",
                lambda record: record.__setitem__("artifact_sha256", []),
                "non-empty mapping",
            ),
            (
                "artifact empty mapping",
                lambda record: record.__setitem__("artifact_sha256", {}),
                "non-empty mapping",
            ),
            (
                "artifact boolean digest",
                lambda record: record["artifact_sha256"].__setitem__(
                    artifact_name, True
                ),
                "artifact_sha256",
            ),
            (
                "artifact short digest",
                lambda record: record["artifact_sha256"].__setitem__(
                    artifact_name, "0" * 63
                ),
                "artifact_sha256",
            ),
        )

        for label, mutate, message in mutations:
            broken = copy.deepcopy(self.manifest["frozen_champion"])
            mutate(broken)
            with (
                self.subTest(case=label),
                self.assertRaisesRegex(
                    champion.ChampionVerificationError,
                    message,
                ),
            ):
                champion.verify_frozen_champion(broken)

    def test_artifact_map_requires_nonempty_string_keys(self) -> None:
        broken = copy.deepcopy(self.manifest["frozen_champion"])
        digest = next(iter(broken["artifact_sha256"].values()))
        broken["artifact_sha256"] = {1: digest}
        with self.assertRaisesRegex(
            champion.ChampionVerificationError, "keys must be non-empty strings"
        ):
            champion.verify_frozen_champion(broken)

    def test_advanced_origin_tracking_ref_does_not_break_immutable_integrity(
        self,
    ) -> None:
        frozen = self.manifest["frozen_champion"]
        real_git = champion._git
        advanced_sha = "f" * 40

        def advanced_origin(repo, *arguments):
            if arguments == ("rev-parse", "refs/remotes/origin/main"):
                return advanced_sha.encode()
            return real_git(repo, *arguments)

        with patch.object(champion, "_git", side_effect=advanced_origin):
            result = champion.require_frozen_champion(frozen)

        self.assertTrue(result["static_integrity_passed"])
        self.assertEqual(result["failures"], [])
        self.assertNotIn("origin_main", [check["id"] for check in result["checks"]])
        observation = result["provenance_state"]["origin_main_tracking_ref"]
        self.assertEqual(observation["status"], "differs_from_frozen_declaration")
        self.assertEqual(observation["observed_sha"], advanced_sha)
        self.assertFalse(observation["matches_declared_frozen_sha"])
        self.assertFalse(observation["integrity_relevant"])
        self.assertEqual(
            result["historical_test_reproduction"]["status"],
            "requires_external_execution",
        )


if __name__ == "__main__":
    unittest.main()
