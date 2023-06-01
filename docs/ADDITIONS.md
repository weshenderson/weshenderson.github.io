# Additions

While fully compliant with [JSON Resume](https://jsonresume.org/) 1.0.0 spec, Alea does utilize a superset of features to further extend the theme. Those additions are outlined below.

## meta

* `siteAuthor`: Sets site author HTML element.
* `siteDescription`: Sets site description  HTML element.
* `siteIcon`: Sets site icon HTML element.
* `siteThumbnail`: Sets site thumbnail HTML element.
* `siteTwitter`: Sets site twitter author card HTML element.
* `siteTags`: Sets site tag(s) HTML element.
* `googleAnalytics`: Optional string: Configures Google Analytics with the provided ID.
* `emailSubject`: Optional string: Sets the email subject line.

## education

* `location`: Sets the location of the provided institution.

## certificate

* `license`: Sets the license number of the certificate.

## work

* `currentEmployee`: Optional bool: Sets `Present` rather than an end date for the employer.
