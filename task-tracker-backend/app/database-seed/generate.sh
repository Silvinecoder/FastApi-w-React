#!/bin/bash

# ------------------------------------------
CURRENT_DIR=$(pwd)
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null && pwd )"
# ------------------------------------------

# Go to generators folder to run db_generator.py
cd "${DIR}/../generators" || exit 1

# Generate schema SQL to seed file in database-seed/ as 02-seed.sql directly
python db_generator.py > "${DIR}/02-seed.sql"
if [[ $? -ne 0 ]]; then
  echo "Failed to generate DB schema"
  exit 1
fi

# Back to database-seed folder
cd "${DIR}" || exit 1

# Concatenate insert SQL files if they exist
if ls -1 ${DIR}/[0-9]*.inserts.*.sql >/dev/null 2>&1; then
  ls -1 ${DIR}/[0-9]*.inserts.*.sql | sort -V | xargs cat > "${DIR}/inserts.sql"
else
  touch "${DIR}/inserts.sql"
fi

# Generate drop.sql based on tables in 02-seed.sql
grep "CREATE TABLE" "${DIR}/02-seed.sql" | awk '{print "DROP TABLE IF EXISTS "$3";"}' > "${DIR}/01-drop.sql"

# Append inserts to 02-seed.sql
echo "

-- Inserts
" >> "${DIR}/02-seed.sql"
cat "${DIR}/inserts.sql" >> "${DIR}/02-seed.sql"

# Clean up
rm "${DIR}/inserts.sql"

echo "seed.sql and drop.sql generated successfully in ${DIR}"