# dshawth

Using the [common crawl](https://registry.opendata.aws/commoncrawl/) from September 2019.

## dependencies

## retrieve one file for testing

```bash
wget https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-39/warc.paths.gz
wget "https://commoncrawl.s3.amazonaws.com/$(zcat warc.paths.gz | head -n1)"
```