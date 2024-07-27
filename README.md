# STO Server Status Discord Bot

This is a Discord Bot for reporting news posts for Star Trek Online. Originally this
was designed to also report Server Status and that may also be added in the future.

## Usage

```bash
docker compose up
```

## Configuration

The .env file supports the following options:

| Key | Description |
| --- | --- |
| STO_SERVER_STATUS_CHANNELS | A comma delimited list of Channel IDs the Bot will report news to. |
| STO_SERVER_STATUS_TOKEN | The Discord API Token associated with your Bot |



