# Euphoric Events: artist booking process (DRAFT textual statement)

> Proposed by the scaffold to satisfy BPMN task 2. The group must approve or replace it. Requirements: at least one external actor, the RDBMS of the first project with artifacts and a dedicated swim lane, at least 10 steps before terminating.

When the line-up planning period for a festival opens, the booking office of Euphoric Events starts booking artists. First, the festival database is queried to retrieve the stages of the festival and their free time slots. Based on this information, the program manager shortlists the artists to invite.

The booking office sends a booking proposal to the first artist of the shortlist (the artist, or their management, is an external actor). The artist evaluates the proposal and replies with an acceptance or a decline. If a decline arrives, or no answer arrives within 5 days, the booking office moves to the next shortlisted artist; if no other artist is left, the process ends without a booking.

When an acceptance arrives, the performance is registered in the database (Performance and PerformanceArtist tables). The program manager assigns the stage and the time slot, and the schedule is updated in the database. The booking office then sends the contract to the artist, who signs it and sends it back. Once the signed contract is received, the line-up update is published (sub-process), and the process ends with the artist booked.

Steps on the successful path (start to end): line-up planning opens, query stages and free slots, shortlist artists, (merge), send booking proposal, (event-based gateway), acceptance received, register performance, assign stage and time slot, update schedule, send contract, signed contract received, publish line-up update (sub-process), artist booked. That is 12 activities and events, excluding the 2 gateways.
