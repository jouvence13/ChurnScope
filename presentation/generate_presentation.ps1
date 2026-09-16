<#
.SYNOPSIS
    Regenere le support de soutenance ChurnScope (presentation/soutenance_churnscope.pptx).

.DESCRIPTION
    Ce script est un simple point d'entree Windows pour generate_presentation.py.
    Il installe python-pptx si necessaire puis reconstruit le fichier .pptx a partir
    des resultats reels et verifies du projet (voir docs/01_analyse_preparation.md,
    docs/02_apprentissage_modeles.md et docs/03_validation_conclusion.md).

    Le .pptx genere n'est pas versionne dans Git (voir .gitignore) : il doit etre
    regenere localement avant chaque soutenance avec ce script.

.EXAMPLE
    .\presentation\generate_presentation.ps1
#>

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$generator = Join-Path $scriptDir "generate_presentation.py"

Write-Host "Verification de python-pptx..." -ForegroundColor Cyan
python -c "import pptx" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "python-pptx n'est pas installe, installation en cours..." -ForegroundColor Yellow
    python -m pip install python-pptx
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Echec de l'installation de python-pptx."
        exit 1
    }
}

Write-Host "Generation de la presentation..." -ForegroundColor Cyan
python $generator
if ($LASTEXITCODE -ne 0) {
    Write-Error "Echec de la generation de la presentation."
    exit 1
}

Write-Host "Termine. Fichier disponible dans presentation\soutenance_churnscope.pptx" -ForegroundColor Green
