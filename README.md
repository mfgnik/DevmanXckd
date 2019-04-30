# Comics publisher
Script to download comics from Xckd and post it to group [VK](https://vk.com)


## How to install
Install the packages from requirements.txt using pip:
```bash
pip3 install -r requirements.txt
```
Then you should create group and app VK and for app vk get access token using [Implicit Flow](https://vk.com/dev/implicit_flow_user).
Parameter scope should be equal photos,groups,wall,offline. Redirect url should be empty.
After this steps add to .env file two lines:
```bash
access_token=TOKEN_YOU_GET
group_id=YOUR_GROUP_ID
```
, where TOKEN_YOU_GET and YOUR_GROUP_ID is your token and group id.

## Project Goals
The code is written for educational purposes on online-course for web-developers dvmn.org.
