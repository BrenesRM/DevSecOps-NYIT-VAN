param(
    [string]$Owner = "BrenesRM",
    [string]$Repo = "DevSecOps-NYIT-VAN",
    [ValidateSet("open", "closed", "dismissed", "fixed", "all")]
    [string]$State = "open",
    [string]$OutputDir = ".\\reports",
    [ValidateSet("csv", "xlsx", "both")]
    [string]$Format = "both"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-GitHubToken {
    if ($env:GITHUB_TOKEN) {
        return $env:GITHUB_TOKEN
    }

    $gh = Get-Command gh -ErrorAction SilentlyContinue
    if ($gh) {
        try {
            $token = gh auth token 2>$null
            if ($token) {
                return $token.Trim()
            }
        }
        catch {
            # Ignore and continue to the explicit error below.
        }
    }

    throw "No se encontro token. Define GITHUB_TOKEN o inicia sesion con GitHub CLI (gh auth login)."
}

function Normalize-State {
    param([string]$ApiState)

    if ($ApiState -eq "all") {
        return ""
    }

    return $ApiState
}

function Get-CodeScanningAlerts {
    param(
        [string]$ApiOwner,
        [string]$ApiRepo,
        [string]$ApiState,
        [hashtable]$ApiHeaders
    )

    $page = 1
    $perPage = 100
    $allAlerts = @()

    do {
        $stateQuery = Normalize-State -ApiState $ApiState
        if ([string]::IsNullOrWhiteSpace($stateQuery)) {
            $url = "https://api.github.com/repos/$ApiOwner/$ApiRepo/code-scanning/alerts?per_page=$perPage&page=$page"
        }
        else {
            $url = "https://api.github.com/repos/$ApiOwner/$ApiRepo/code-scanning/alerts?state=$stateQuery&per_page=$perPage&page=$page"
        }

        Write-Host "Consultando pagina $page ..."
        $response = Invoke-RestMethod -Uri $url -Headers $ApiHeaders -Method Get

        if ($null -eq $response) {
            $batch = @()
        }
        elseif ($response -is [System.Array]) {
            $batch = $response
        }
        else {
            $batch = @($response)
        }

        $allAlerts += $batch
        $page++
    } while ($batch.Count -eq $perPage)

    return $allAlerts
}

function ConvertTo-ReviewRows {
    param([array]$Alerts)

    return $Alerts | ForEach-Object {
        $location = $null
        if ($_.most_recent_instance -and $_.most_recent_instance.location) {
            $location = $_.most_recent_instance.location
        }

        [PSCustomObject]@{
            AlertNumber    = $_.number
            State          = $_.state
            RuleId         = $_.rule.id
            RuleSeverity   = $_.rule.severity
            SecuritySeverity = $_.rule.security_severity_level
            Tool           = $_.tool.name
            FilePath       = if ($location) { $location.path } else { $null }
            StartLine      = if ($location) { $location.start_line } else { $null }
            EndLine        = if ($location) { $location.end_line } else { $null }
            CreatedAt      = $_.created_at
            UpdatedAt      = $_.updated_at
            HtmlUrl        = $_.html_url
        }
    }
}

function Export-XlsxIfPossible {
    param(
        [array]$Rows,
        [string]$XlsxPath
    )

    $importExcel = Get-Module -ListAvailable -Name ImportExcel
    if (-not $importExcel) {
        Write-Warning "Modulo ImportExcel no encontrado. Se omitira salida XLSX."
        return $false
    }

    $Rows | Export-Excel -Path $XlsxPath -WorksheetName "Alerts" -AutoSize -TableName "CodeScanningAlerts" -FreezeTopRow
    return $true
}

try {
    $token = Get-GitHubToken

    if (-not (Test-Path -Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir | Out-Null
    }

    $headers = @{
        Authorization        = "Bearer $token"
        Accept               = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
    }

    $alerts = Get-CodeScanningAlerts -ApiOwner $Owner -ApiRepo $Repo -ApiState $State -ApiHeaders $headers
    $rows = ConvertTo-ReviewRows -Alerts $alerts

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $baseName = "code_scanning_${Owner}_${Repo}_${State}_$timestamp"
    $csvPath = Join-Path $OutputDir "$baseName.csv"
    $xlsxPath = Join-Path $OutputDir "$baseName.xlsx"

    if ($Format -eq "csv" -or $Format -eq "both") {
        $rows | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
        Write-Host "CSV generado: $csvPath"
    }

    if ($Format -eq "xlsx" -or $Format -eq "both") {
        $ok = Export-XlsxIfPossible -Rows $rows -XlsxPath $xlsxPath
        if ($ok) {
            Write-Host "XLSX generado: $xlsxPath"
        }
    }

    Write-Host "Total alertas exportadas: $($rows.Count)"
}
catch {
    Write-Error $_
    exit 1
}
