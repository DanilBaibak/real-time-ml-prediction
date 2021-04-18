CREATE TABLE IF NOT EXISTS predictions
(
    id SERIAL PRIMARY KEY,
    crim float(8) NOT NULL,
    zn float(8) NOT NULL,
    indus float(8) NOT NULL,
    chas smallint NOT NULL,
    nox float(8) NOT NULL,
    rm float(8) NOT NULL,
    age float(8) NOT NULL,
    dis float(8) NOT NULL,
    rad smallint NOT NULL,
    tax float(8) NOT NULL,
    ptratio float(8) NOT NULL,
    b float(8) NOT NULL,
    lstat float(8) NOT NULL,
    prediction float(8) NOT NULL,
    pipeline_version varchar(32) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
