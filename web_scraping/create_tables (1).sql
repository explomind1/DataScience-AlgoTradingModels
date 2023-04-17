CREATE TABLE hotteststocks (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    is_etf BOOLEAN NOT NULL
);

CREATE TABLE mention_wallstreet (
    stock_id INTEGER,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    message TEXT NOT NULL,
    source TEXT NOT NULL, 
    url TEXT NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES hotteststocks (id)
);
CREATE INDEX ON mention_wallstreet (stock_id, dt DESC);
SELECT create_hypertable('mention_wallstreet', 'dt');

CREATE TABLE mention_stocks (
    stock_id INTEGER,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    message TEXT NOT NULL,
    source TEXT NOT NULL, 
    url TEXT NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES hotteststocks (id)
);

CREATE INDEX ON mention_stocks (stock_id, dt DESC);
SELECT create_hypertable('mention_stocks', 'dt');


CREATE TABLE etf_holding (
    etf_id INTEGER NOT NULL, 
    holding_id INTEGER NOT NULL,
    dt DATE NOT NULL, 
    shares NUMERIC,
    weight NUMERIC, 
    PRIMARY KEY (etf_id, holding_id, dt),
    CONSTRAINT fk_etf FOREIGN KEY (etf_id) REFERENCES stock (id),
    CONSTRAINT fk_holding FOREIGN KEY (holding_id) REFERENCES stock (id)
);

CREATE TABLE stock_price (
    stock_id INTEGER NOT NULL,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    open NUMERIC (6,2) NOT NULL, 
    high NUMERIC (6,2) NOT NULL,
    low NUMERIC (6,2) NOT NULL,
    close NUMERIC (6,2) NOT NULL, 
    volume NUMERIC NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);

CREATE INDEX ON stock_price (stock_id, dt DESC);

SELECT create_hypertable('stock_price', 'dt');