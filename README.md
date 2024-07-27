# STO Server Status Discord Bot

This is a Discord Bot for reporting news posts for Star Trek Online. Originally this
was designed to also report Server Status and that may also be added in the future.

## Inviting this bot to your server

This bot may be invited to your discord server using the following link:

https://discord.com/oauth2/authorize?client_id=776531512606195742


## Usage

```bash
docker compose up
```

## Configuration

The .env file supports the following options:

| Key | Default | Description |
| --- | --- | --- |
| STO_SERVER_STATUS_TOKEN |  | The Discord API Token associated with your Bot |
| STO_SERVER_STATUS_CHANNEL | sto-news | The Discord Bot Will Send New STO news to channels matching this name |


