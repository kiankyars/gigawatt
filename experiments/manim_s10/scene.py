from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup,
    Circle,
    FadeIn,
    Line,
    Rectangle,
    Scene,
    ShowPassingFlash,
    Text,
    VGroup,
    VMobject,
    config,
)

EXPERIMENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_DIR.parents[1]
sys.path.insert(0, str(EXPERIMENT_DIR))

from manifest import Pilot, Transformation, load_pilot

TOKENS = runpy.run_path(REPO_ROOT / "src/gigawatt/tokens.py")
INK = TOKENS["INK"]
PAPER = TOKENS["PAPER"]
MUTED = TOKENS["MUTED_TEXT"]
FAINT = TOKENS["FAINT_GUIDE"]
THERMAL = TOKENS["THERMAL"]

config.background_color = PAPER

NODE_FILL = {
    "die": THERMAL["die_heat"],
    "cold_plate": THERMAL["technology_return"],
    "rack_manifold": THERMAL["technology_supply"],
    "rack_air_load": THERMAL["air"],
}
EDGE_COLOR = {
    "die_to_cold_plate_heat": THERMAL["die_heat"],
    "cold_plate_to_manifold_return": THERMAL["technology_return"],
    "manifold_to_cold_plate_supply": THERMAL["technology_supply"],
}
LABEL_OFFSETS = {
    "die": np.array([-0.65, -0.60, 0.0]),
    "cold_plate": np.array([-1.15, 0.55, 0.0]),
    "rack_manifold": np.array([0.35, -0.72, 0.0]),
    "rack_air_load": np.array([-0.10, 0.62, 0.0]),
}


def project(point: list[float]) -> np.ndarray:
    x, y, z = point
    return np.array(
        [
            (x - 600.0) * 0.035 + z * 0.015,
            (y - 45.0) * 0.040 - z * 0.018,
            0.0,
        ]
    )


def node_center(pilot: Pilot, node_id: str) -> np.ndarray:
    return project(pilot.scene_nodes[node_id]["at"])


def make_node(pilot: Pilot, node_id: str) -> VGroup:
    center = node_center(pilot, node_id)
    color = NODE_FILL[node_id]
    if node_id == "rack_manifold":
        body = VGroup(
            Line(
                [-0.38, -0.12, 0],
                [0.38, -0.12, 0],
                color=THERMAL["technology_supply"],
                stroke_width=8,
            ),
            Line(
                [-0.38, 0.12, 0],
                [0.38, 0.12, 0],
                color=THERMAL["technology_return"],
                stroke_width=8,
            ),
        )
    elif node_id == "rack_air_load":
        enclosure = Rectangle(width=0.86, height=0.58, color=INK, stroke_width=2)
        fan = Circle(radius=0.15, color=color, stroke_width=5)
        body = VGroup(enclosure, fan)
    elif node_id == "cold_plate":
        body = Rectangle(
            width=0.82,
            height=0.18,
            color=color,
            fill_color=color,
            fill_opacity=0.78,
            stroke_width=2,
        )
    else:
        body = Rectangle(
            width=0.48,
            height=0.32,
            color=color,
            fill_color=color,
            fill_opacity=0.88,
            stroke_width=2,
        )
    body.move_to(center)
    label = Text(
        pilot.node_labels[node_id], font="Helvetica Neue", font_size=20, color=INK
    )
    label.move_to(center + LABEL_OFFSETS[node_id])
    return VGroup(body, label)


def make_edge(pilot: Pilot, edge_id: str) -> VMobject:
    points = [project(point) for point in pilot.scene_edges[edge_id]["points"]]
    edge = VMobject(color=EDGE_COLOR[edge_id], stroke_width=4)
    edge.set_points_as_corners(points)
    return edge


class TransformationClip(Scene):
    def construct(self) -> None:
        pilot = load_pilot()
        transformation_id = os.environ.get("GIGAWATT_TRANSFORMATION_ID")
        if not transformation_id:
            available = ", ".join(item.id for item in pilot.transformations)
            raise ValueError("set GIGAWATT_TRANSFORMATION_ID to one of: " + available)
        transformation = pilot.transformation(transformation_id)
        self._render_transformation(pilot, transformation)

    def _render_transformation(
        self, pilot: Pilot, transformation: Transformation
    ) -> None:
        title = Text(
            transformation.title,
            font="Helvetica Neue",
            font_size=38,
            weight="BOLD",
            color=INK,
        ).to_edge(np.array([0.0, 1.0, 0.0]), buff=0.42)
        state_id = Text(
            transformation.id,
            font="Helvetica Neue",
            font_size=18,
            color=MUTED,
        ).next_to(title, np.array([0.0, -1.0, 0.0]), buff=0.12)
        source_id = Text(
            f"source {pilot.source_digest}",
            font="Helvetica Neue",
            font_size=11,
            color=MUTED,
        ).to_edge(np.array([0.0, -1.0, 0.0]), buff=0.20)

        rack_boundary = Rectangle(
            width=6.7,
            height=4.3,
            color=FAINT,
            stroke_width=2,
        ).shift(np.array([0.15, -0.32, 0.0]))
        boundary_label = Text(
            "RACK-PACKAGE BOUNDARY",
            font="Helvetica Neue",
            font_size=17,
            color=MUTED,
        ).next_to(rack_boundary, np.array([-1.0, 0.0, 0.0]), buff=-1.72)
        boundary_label.shift(np.array([0.0, 1.88, 0.0]))

        nodes = {node_id: make_node(pilot, node_id) for node_id in pilot.scene_nodes}
        edges = {edge_id: make_edge(pilot, edge_id) for edge_id in pilot.scene_edges}

        for node_id, node in nodes.items():
            node.set_opacity(
                0.16 if node_id not in transformation.focus_nodes else 0.30
            )
        for edge_id, edge in edges.items():
            edge.set_opacity(
                0.10 if edge_id not in transformation.focus_edges else 0.24
            )

        self.add(
            rack_boundary,
            boundary_label,
            source_id,
            *edges.values(),
            *nodes.values(),
        )
        self.play(FadeIn(title), FadeIn(state_id))

        focus_animations = []
        for node_id in transformation.focus_nodes:
            focus_animations.append(nodes[node_id].animate.set_opacity(1.0))
        for edge_id in transformation.focus_edges:
            focus_animations.append(
                edges[edge_id].animate.set_stroke(width=5).set_opacity(1.0)
            )
        if focus_animations:
            self.play(AnimationGroup(*focus_animations, lag_ratio=0.06))

        if transformation.pulse_edges:
            self.play(
                AnimationGroup(
                    *[
                        ShowPassingFlash(
                            edges[edge_id].copy().set_stroke(width=10),
                            time_width=0.32,
                        )
                        for edge_id in transformation.pulse_edges
                    ],
                    lag_ratio=0.18,
                )
            )
        self.wait()
