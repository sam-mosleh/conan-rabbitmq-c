# Conan-RabbitMQ-C

Conan C/C++ package for [RabbitMQ-C](https://github.com/alanxz/rabbitmq-c) library.

| Bintray | Travis | Appveyor |
|---------|--------|----------|
|[ ![Download](https://api.bintray.com/packages/sam-mosleh/conan/rabbitmq-c:mosleh/images/download.svg?version=0.10.0:stable) ](https://bintray.com/sam-mosleh/conan/rabbitmq-c:mosleh/0.10.0:stable/link)|[![Build Status](https://travis-ci.com/sam-mosleh/conan-rabbitmq-c.svg?branch=release%2F0.10.0)](https://travis-ci.com/sam-mosleh/conan-rabbitmq-c)|[![Build status](https://ci.appveyor.com/api/projects/status/r30veyik8o24yyev/branch/release/0.10.0?svg=true)](https://ci.appveyor.com/project/sam-mosleh/conan-rabbitmq-c/branch/release/0.10.0)|



## Getting Started

In order to use this package you have to add my repo to your remote list.
```
conan remote add mosleh-repo https://api.bintray.com/conan/sam-mosleh/conan
```

### Installation

For basic package installation:

```
conan install rabbitmq-c/0.10.0@mosleh/stable
```

### Options

Key | Default Value | Description
--- | --- | :--
`shared` | true | Use dynamic linkage
`ssl` | true | Enables SSL for the package

Read about [options](https://docs.conan.io/en/latest/creating_packages/getting_started.html?highlight=options#settings-vs-options).

## License

This project is licensed under the **MIT License** - see the [LICENSE](https://github.com/alanxz/rabbitmq-c/blob/master/LICENSE-MIT) file for details
