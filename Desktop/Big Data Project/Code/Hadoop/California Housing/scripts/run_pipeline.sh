#!/bin/bash
set -e

STREAMING_JAR=$(find /usr/local/hadoop -name "hadoop-streaming*.jar" | head -1)
BASE=~/ca_house_price_mr
EPOCHS=10

echo "Step 1: Upload data to HDFS"
hdfs dfs -mkdir -p /user/hadoop/ca_housing/input
hdfs dfs -rm -f /user/hadoop/ca_housing/input/california_housing.csv 2>/dev/null || true
hdfs dfs -put $BASE/data/california_housing.csv /user/hadoop/ca_housing/input/

echo "Step 2: Job 1 — Normalize"
hdfs dfs -rm -r -f /user/hadoop/ca_housing/stats
hadoop jar $STREAMING_JAR \
    -files $BASE/src/normalize_mapper.py,$BASE/src/normalize_reducer.py \
    -mapper "python3 normalize_mapper.py" \
    -reducer "python3 normalize_reducer.py" \
    -input /user/hadoop/ca_housing/input \
    -output /user/hadoop/ca_housing/stats
hdfs dfs -getmerge /user/hadoop/ca_housing/stats $BASE/stats.txt

echo "Step 3: Initialize weights"
python3 -c "import json; json.dump({'weights':[0.0]*8,'bias':0.0}, open('$BASE/weights.txt','w'))"

echo "Step 4: Job 2 — Gradient descent ($EPOCHS epochs)"
for EPOCH in $(seq 1 $EPOCHS); do
    echo "  Epoch $EPOCH..."
    hdfs dfs -rm -r -f /user/hadoop/ca_housing/grad_$EPOCH
    hadoop jar $STREAMING_JAR \
        -files $BASE/src/gradient_mapper.py,$BASE/src/gradient_reducer.py,$BASE/weights.txt,$BASE/stats.txt \
        -mapper "python3 gradient_mapper.py" \
        -reducer "python3 gradient_reducer.py" \
        -input /user/hadoop/ca_housing/input \
        -output /user/hadoop/ca_housing/grad_$EPOCH
    [ -f $BASE/weights_new.txt ] && mv $BASE/weights_new.txt $BASE/weights.txt
done

echo "Step 5: Job 3 — Predict"
hdfs dfs -rm -r -f /user/hadoop/ca_housing/predictions
hadoop jar $STREAMING_JAR \
    -files $BASE/src/predict_mapper.py,$BASE/weights.txt,$BASE/stats.txt \
    -mapper "python3 predict_mapper.py" \
    -reducer "cat" \
    -input /user/hadoop/ca_housing/input \
    -output /user/hadoop/ca_housing/predictions
hdfs dfs -getmerge /user/hadoop/ca_housing/predictions $BASE/predictions_raw.txt

echo "Step 6: Evaluate"
python3 $BASE/src/evaluate_reducer.py < $BASE/predictions_raw.txt | tee $BASE/output/evaluation_results.txt

echo ""
echo "Done! Results saved to $BASE/output/evaluation_results.txt"
