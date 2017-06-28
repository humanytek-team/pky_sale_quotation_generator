# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added
- Add new wizard, for now only just request the material (product) to use for the quotation to generate for the new product to be manufactured.
- Data of products demo added.
- Improve view of wizard adding all fields of section material.
- Add new fields to model of wizard for calculate length of material in millimeters and calculate total of thousands of the new product in the quotation to generate.
- Add new field "computed current_rate_usd" to show the current rate of currency USD in the wizard.
- Add new fields that allow capture data about the inks to use to produce the new product to quote.
- Add new field "Glue and Other Spenses".
- Add new fields and calculations. The wizard allows to capture all the necessary information and make the corresponding calculations to generate the quotes.
- Add field "Range of Prices to Quote" to model of wizard. This field allows show a table (tree) in wizard to register the range of prices per thousand to send to quote.
- Computation of sale price works correctly also if the user does not indicate costs of inks, glue ant other expenses.
- Add field customer to wizard and method generate_quotations to process the data of the wizard and generate the quotation in the system.
- Adds the field "Shrinkage Percentage" to include it in the computation of total of thousands to be quoted.
- The wizard sets USD as currency for the product to be created for the quotation.
