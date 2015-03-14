# Introduction #

Please use this page to talk about any engine issues, decisions, and developments that crop up. If you plan to or are thinking about making any major changes, make sure to converse with the rest of the group.


# Details #

3/21/10
Yeah everything is rectangles now (as of a few days ago actually, but I do not remember to update these things). Collision is much simpler and working fine.

3/16/10
Because the current design of our polygon-driven collision engine is too complex, I am considering moving to a rectangle-only collision engine. Collision code can be further simplified by not testing for collision before the event; it may be better to simply record the object's last position to make sure it didn't go through anything. Lasers and other "instant" projectiles can have straight lines to test for collision rather than moving boxes. For fast-moving projectiles that are not instant it will be necessary to code in checks to make sure they did not pass through anything.