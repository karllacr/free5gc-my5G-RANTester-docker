NT=$1

for i in $(seq $NT)
do
    rm config/tester$i.yaml
done

rm n-testers-compose.yaml
