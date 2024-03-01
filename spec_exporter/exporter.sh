read -p "Enter DTO uppercase: " DTO
read -p "Enter KIND: " KIND

if [ -z "$DTO" ] || [ -z "$KIND" ]; then
    echo "Error: DTO and KIND must be provided"
    exit 1
fi

BASE_API=http://192.168.49.2:30180/api/v1/schemas
curl $BASE_API/$DTO/$KIND | jq -r ".schema" > ${DTO}_${KIND}.json
datamodel-codegen   --input ${DTO}_${KIND}.json \
                    --input-file-type jsonschema \
                    --output ${DTO}_${KIND}.py \
                    --output-model-type pydantic.BaseModel \
                    --field-constraints \
                    --target-python-version 3.9 \
                    --use-standard-collection \
                    --use-schema-description
rm ${DTO}_${KIND}.json
