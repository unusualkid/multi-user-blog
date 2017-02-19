# Project Multi-User Blog
Multi-User Blog is a project created on Google App Engine (GAE) that displays blog posts, comments, likes, edit and delete features based on the user login. User can create new logins via signup, but have to enter valid inputs.

## Installation

1. Install [Google App Engine](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
2. Sign up for a [Google App Engine Account](https://console.cloud.google.com/appengine/)
3. Create a new project in [Google Developer Console](https://console.cloud.google.com/)

## To Run the Original Deployed Version
> Go to `https://multi-user-blog-159211.appspot.com/blog`

## To Run Tests Locally
1. Navigate to your developing directory, where you put the `app.yaml` file
2. Run `dev_appserver .`
3. Go to `localhost:8080` to deploy web app
4. Go to `localhost:8080` to admin database and app

## To Deploy Your Own Version on Internet
1. Once your web app is ready for deployment, nagivate to the developing directory.
2. `gcloud app deploy` in the command line and follow the instructions.

## Other Resources
- [Jinja2 Documentation](http://jinja.pocoo.org/docs/2.9/)

### Author
> Kenneth Chen
### Thanks to
> This project is part of the [Udacity Full Stack Program](https://classroom.udacity.com/nanodegrees/nd004/syllabus).