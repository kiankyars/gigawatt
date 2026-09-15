import { rapidBuildScenes } from "./rapid-build-cases.js";

// A selected modular-construction case within Chapter 13.
export const scenes = rapidBuildScenes.filter(scene => scene.id === "aws-houdini-prefab");
