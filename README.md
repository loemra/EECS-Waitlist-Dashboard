# UMICH Waitlist Dashboard

CS classes at UMich are notorious for filling up within the first couple registration dates. This dashboard is for helping you make an informed decision about which classes to register for. All upper-level EECS classes are shown along with their waitlist status, if a class is waitlisted it will also display how many people are on the waitlist. There is also easy Atlas access with links for each class to learn more.

## Link: 
https://waitlist-dashboard.fly.dev/
### Must have umich account to use.

## Example:
![example](https://github.com/loemra/EECS-Waitlist-Dashboard/assets/112432339/18195b30-b946-4723-885f-9931805130c9)

## How to use:
<ol>
    <li>Go to <a href="https://atlas.ai.umich.edu/" target="_blank">https://atlas.ai.umich.edu/</a></li>
    <li>Make sure you are logged in.</li>
    <li>Right click anywhere on the page and press inspect.<br></li>
    <img src="https://github.com/loemra/EECS-Waitlist-Dashboard/assets/112432339/ae3a028b-fbb5-47dd-a80d-d304bd39543c" alt="Inspect">
    <li>Navigate to the network tab.<br></li>
    <img src="https://github.com/loemra/EECS-Waitlist-Dashboard/assets/112432339/2e238810-772d-4fc5-80dd-07af01623455" alt="Network">
    <li>Refresh the page.</li>
    <li>Select any request with the <code>atlas.ai.umich.edu</code> domain.</li>
    <li>Navigate to the Cookies tab.</li>
    <li>Scroll down until you find <code>sessionid</code> and copy the value.<br></li>
    <img src="https://github.com/loemra/EECS-Waitlist-Dashboard/assets/112432339/36655fdd-cad8-4d98-806a-7f68540737ac" alt="Cookies">
    <li>You’re done! Use that sessionid to authenticate in the dashboard.</li>
</ol>


## TO-DO:
- Allow users to add custom classes to their dashboard.
- Allow re-ordering of classes.
- Try and find a way around using Atlas sessionids.
    - Transition to this API: https://dir.api.it.umich.edu/
