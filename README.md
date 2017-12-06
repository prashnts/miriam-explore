[![miriam.noop.pw](docs/gh-banner.png)](https://miriam.noop.pw)

miRiam provides access to interaction networks of mRNA translation regulation through intronic miRNAs under various tissue-specific cellular contexts.
This repo contains source code for the network.

## Quickstart
Server is written using `django`, and in `python 3.6`. Client-side code is compiled using `brunch`.

Overall, the following sums up the steps to get the server up and running:

- Install js packages using `yarn install` or `npm install`.
- Build client js using `npm run build`.
- It's recommended to create and activate a new `Python 3.6` environment using `virtual-environment` or `py-env`.
- Next, install python packages using `pip install -r requirements.txt`.
- This server requires a couple of environment variables that are described in `.env.sample`. Substitute valid values for your environment, and source it in your shell session.
- On first setup you will need to download serialized dataset. A link to that is provided below.
- Run the server using `./manage.py runserver`.

## License
MIT
