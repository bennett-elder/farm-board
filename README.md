# Intro
Introducing FARM-Board - FastAPI, React & MongoDB quick status board

# Components

## Poster
* Endpoint accepting only HTTP POSTs
* Requires API key
* Keys can be passed by environment variable or loaded from Mongodb

## Viewer
* React frontend and FastAPI backend to show posts and comments
* No authentication: secure it with a private network and VPN

## Notifier
* [mongo-narc](https://github.com/bennett-elder/mongo-narc) watches a Mongodb collection and Slack notifies

# Getting started

```
docker run -it \
  -e APP_MODE=poster
  -e DB_NAME=$DB_NAME \
  -e DB_URL=$DB_URL \
  -e API_KEYS="USE TABLE" \
  bennettelder/farm-board:latest

docker run -it \
  -e APP_MODE=viewer
  -e DB_NAME=$DB_NAME \
  -e DB_URL=$DB_URL \
  bennettelder/farm-board:latest

docker run -it \
  -e DB_NAME=$DB_NAME \
  -e DB_URL=$DB_URL \
  -e SLACK_URL=$SLACK_URL \
  -e MATCH_STRING=$MATCH_STRING \
  bennettelder/mongo-narc:latest
```

# Environment Variable Config

## Shared between Viewer and Poster

* PORT

  default: 8000

  Server port

* APP_MODE

  default: poster

  poster or viewer

* DB_NAME

  database name

* DB_URL

  database server URL with credentials

## Poster Only

* API_KEYS

  csv list of keys or 'USE TABLE' to load keys from a collection named 'api-keys'

## Viewer Only

* FRONTEND_TITLE

  default: FARM Board

* FRONTEND_SHORTNAME

  default: farm-board

* FRONTEND_DESCRIPTION

  default: Status board built with Fast API React Mongodb

* FRONTEND_POSTS_NAME

  default: FARM Board Posts

## Notifier

* DB_NAME

  database name

* DB_URL

  database server URL with credentials


* SLACK_URL

  slack webhook URL

* MATCH_STRING

  string to watch for in mongodb table


* REPORT_MESSAGE

  string to send in slack message, prefaced by the id


* DATE_COLUMN_NAME 

  column it is tracking to make sure it doesn't renotify about old messages after startup

* ID_COLUMN_NAME 

  column to use as the value for the slack notification prefix

* REPORT_MESSAGE to send for the notification

  message sent in notification, prefixed by value from ID_COLUMN_NAME

* WAIT_BETWEEN_CHECKS

  how long to WAIT_BETWEEN_CHECKS
