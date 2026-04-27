@echo off
title Intent Classifier
cls

echo ==========================================
echo      Intent Classifier Automation
echo ==========================================

:: Check if model exists
if not exist "model.pkl" goto no_model

echo Model found.
choice /c YN /n /t 5 /d N /m "Do you want to force retrain? (y/n, default n in 5s): "
if errorlevel 2 goto skip_retrain
if errorlevel 1 goto train_model

:no_model
echo Model not found! Starting training...

:train_model
echo This may take a moment to download datasets...
python train.py
if errorlevel 1 (
    echo Training failed! Exiting.
    exit /b
)
echo Training complete.
goto run_prediction

:skip_retrain
echo Skipping training.

:run_prediction
:: Run Prediction
echo.
echo Starting Prediction Interface...
python predict.py
