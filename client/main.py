from auth import Login, Logout
from token_storage import load_token
from api import get_my_profile

from app.utils.auth import decode_jwt_token


def main():

    # If no token, prompt user to login or sign up
    if not load_token():
        print("Welcome to ChatCLI 👋 \n")

        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        try:
            option = int(input("Select an option: "))
        except ValueError:
            print("Enter a valid option")

        match option:
            case 1:
                Login()

    else:
        # User is logged in
        username = decode_jwt_token(load_token().get("access_token"))

        print(f"Welcome back, {username} 👋 \n")

        print("1. View my profile")
        print("2. Send a message")
        print("3. View messages")
        print("4. View conversations")
        print("5. Logout")

        try:
            option = int(input("Select an option: "))
        except ValueError:
            print("Enter a valid option")

        match option:
            case 1:
                get_my_profile()
            case 5:
                Logout()


"""
You’re actually at a very natural stopping point. Login + token persistence is the first real milestone for a CLI, so good instincts there.

From here, the question isn’t “more auth”, it’s “how does the user interact with the app after auth”.

There are two clean directions you can go, and the choice is more about UX than backend correctness.

Option 1: Interactive CLI (menu / prompt based)

This matches what you already started with:

Welcome to ChatCLI 👋

1. Login
2. Sign up
3. Exit


After login, you keep the process alive and move the user into an authenticated loop.

Rough flow

App starts

Check if token exists

If not → show login/signup menu

If yes → show authenticated menu

Example mental model:

Unauthenticated
 ├─ login
 ├─ signup
 └─ exit

Authenticated
 ├─ send message
 ├─ view history
 ├─ logout
 └─ exit


In code terms, this is just a while True loop with input and branching.

Very simple, very explicit, very easy to reason about.

This style is great if:

you want something chat-like

you want a “session” feeling

users are expected to stay inside the app for a while

Option 2: Command-style CLI (git / gh / docker style)

This is the more “professional” CLI model.

Instead of menus, you do things like:

chatcli login
chatcli send "hello world"
chatcli history
chatcli logout


Each command:

starts

loads the token

makes a request

exits

No persistent loop.

This is better if:

you want scripting support

you want composability

you want something that feels Unix-native

You can still prompt for username/password inside chatcli login, so it’s not less friendly, just different.

Which should you pick right now?

Given where you are and what you’re learning, I’d suggest this progression:

Step 1 (now): Interactive mode first

Why:

you already think in terms of input/output

it makes auth flow very obvious

less mental overhead

easier to debug

You can always refactor later.

Start with something like:

Welcome back, alice 👋

1. Send message
2. Logout
3. Exit


Behind the scenes:

token already exists

every action uses Authorization: Bearer ...

Concrete “next steps” from your current state

You already have:

login endpoint

JWT returned

token saved locally

Here’s what I’d do next, in order:

1. Add “am I logged in?” check

On startup:

if token file exists → treat user as logged in

if not → show login/signup menu

Don’t overthink validation yet. Existence is fine for now.

2. Implement logout

Logout in a CLI is boring, and that’s good.

It just:

deletes the token file

def logout():
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()


No API call required.

3. Make one protected endpoint call

This is the real test that everything works.

For example:

/me

/profile

/messages

Anything that requires Depends(get_current_user).

From the CLI:

load token

attach header

make request

print response

Once this works, your auth pipeline is solid.

4. Only then worry about UX polish

Things like:

better prompts

masking password input

clearer error messages

retry on 401 → force re-login

These come after correctness.

One important mindset shift

Your CLI is not “the backend, but local”.

It is:

a thin client

with state (token)

that orchestrates HTTP calls

and prints results nicely

If you keep that framing, decisions get easier.

My honest suggestion

Start with:

interactive menu

minimal features

one authenticated action

Get that fully working end to end.

Once that feels boring, you’ll know exactly how to turn it into a command-based CLI if you want.

If you want, next we can:

sketch a clean app loop

design the post-login menu

or map your existing API routes to CLI actions

im done with no. 2

Nice. That’s a real checkpoint, not a trivial one.

If logout is done, the auth lifecycle is basically in place. From here, the next correct move is very specific, and it’s not more menus.

The next thing to build: one protected action

You want to prove this end-to-end:

“After login, my CLI can call a protected FastAPI route using the stored token.”

Everything else sits on top of that.

Step 3 (the important one): call a protected endpoint

Pick the simplest authenticated endpoint you have, or add one just for this.

On the API side (example)

Something like:

@app.get("/me")
def me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
    }


Nothing fancy. No business logic.

On the CLI side

You already have:

token saved

token loaded

logout working

Now wire the token into a request.

Conceptually:

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = httpx.get(
    f"{API_BASE_URL}/me",
    headers=headers
)


Then:

print the response

handle 401 cleanly

What success looks like

When this works, you should see:

valid token → endpoint returns user data

deleted/expired token → 401

401 → CLI tells user to log in again

Once this is solid, your auth flow is done.

What not to do yet

Don’t:

add more endpoints

optimize UX

refactor structure

switch to command-based CLI

Those are all distractions until this works.

Step 4 (small but important): centralize requests

Once one protected call works, do this tiny refactor:

def api_client():
    headers = auth_headers()
    return httpx.Client(headers=headers)


Then:

with api_client() as client:
    response = client.get("/me")


This saves you from repeating auth logic everywhere.

Step 5: plug it into your menu loop

Add one option after login:

1. Who am I
2. Logout
3. Exit


That’s enough to prove the architecture.

Big picture check (this matters)

At this point, you will have:

OAuth2 login

JWT storage

automatic auth headers

protected API access

logout

That’s the entire auth story for:

CLIs

SPAs

mobile apps

Everything else is just features.

Tell me this next, very specifically:

do you already have a protected endpoint, or should we add a minimal /me?

are you using httpx sync or async?

We’ll take the next step cleanly, not rushed.
"""
