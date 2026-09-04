# Course direction

GIGAWATT teaches one system: supplying a data center with usable electrical
power and returning its heat to the environment. The learner should finish able
to trace both paths, explain the function of the equipment, calculate a few
useful limits, and recognize which boundary a capacity number describes.

Start with the rack. It makes the rest of the course necessary: the grid must
deliver power, electrical systems must transform and protect it, compute must
turn it into useful work, and cooling must keep moving heat out. Return to that
same system throughout the course so details accumulate into a coherent model.

## What belongs

- Power versus energy, including the boundary between facility and IT load.
- Voltage, current, and loss as the reason for transmission and transformation.
- A generic electrical path from campus connection through distribution to the rack.
- UPS runtime, backup supply, path independence, and capacity during failures.
- Rack and processor power conversion, and the limits of turning MW into compute.
- Component cooling, technology and facility loops, residual air, and heat rejection.
- A final system calculation and a dated case that tests the distinction between
  an announcement, equipment capacity, and operating service.

Generation surveys, financing, procurement, market commentary, and elaborate
project chronologies do not need standalone chapters. Keep only the parts that
clarify the central engineering problem.

## Visual decisions

Every lesson needs a diagram that explains a relationship. Use spatial views
for location and nesting, a schematic for connections, a comparison for a
tradeoff, and a quantitative display for a calculation. Geometry and labels
must stay readable at the actual teaching size.

An interaction earns its place when the learner can predict an outcome, change
an input, observe the result, and explain why. Keep the model's assumptions next
to the result. Do not animate quantities that lack a defined meaning or imply
that display motion is the physical velocity of electricity or coolant.

Keep a consistent power/heat color grammar, visible units, short direct labels,
and a clear distinction between a general teaching model and site evidence.
Treat reduced motion, keyboard access, mobile layout, and text explanations as
part of the visual design.

## Engineering discipline

Equations and assumptions live beside their implementations and are covered by
tests that check known examples and limiting behavior. Sources belong to the
lesson where the claim is used. A generic architecture does not establish a
site's as-built arrangement. Missing quantities stay unknown.

The repository has one editable curriculum and one generated course page.
Keep the build deterministic and the release checks small enough to run on every
change. Teaching quality comes from technical review, using the interactions,
and inspecting the rendered course; historical acceptance labels cannot prove it.
