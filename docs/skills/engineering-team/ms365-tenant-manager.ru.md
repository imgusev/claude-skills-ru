---
title: "Менеджер клиентов Microsoft 365 { #microsoft-365-tenant-manager } — Агентский скилл и плагин Codex"
description: "Администрирование клиента Microsoft 365 для глобальных администраторов. Автоматизируйте настройку клиента M365, задачи администрирования Office 365. Агентский скилл для Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Менеджер клиентов Microsoft 365 { #microsoft-365-tenant-manager }

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Инженерия — базовый уровень</span>
<span class="meta-badge">:material-identifier: `ms365-tenant-manager`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/imgusev/claude-skills-ru/tree/main/engineering-team/skills/ms365-tenant-manager/SKILL.md">Источник</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Установить:</span> <code>claude /plugin install engineering-skills</code>
</div>


Экспертное руководство и автоматизация для глобальных администраторов Microsoft 365, управляющих настройкой клиента, жизненным циклом пользователей, политиками безопасности и оптимизацией организации.

---

## Быстрый старт { #quick-start }

### Запустите аудит безопасности { #run-a-security-audit }

```powershell
Connect-MgGraph -Scopes "Directory.Read.All","Policy.Read.All","AuditLog.Read.All"
Get-MgSubscribedSku | Select-Object SkuPartNumber, ConsumedUnits, @{N="Total";E={$_.PrepaidUnits.Enabled}}
Get-MgPolicyAuthorizationPolicy | Select-Object AllowInvitesFrom, DefaultUserRolePermissions
```

### Массовое предоставление пользователям данных из CSV { #bulk-provision-users-from-csv }

```powershell
# CSV columns: DisplayName, UserPrincipalName, Department, LicenseSku
Import-Csv .\new_users.csv | ForEach-Object {
    $passwordProfile = @{ Password = (New-Guid).ToString().Substring(0,16) + "!"; ForceChangePasswordNextSignIn = $true }
    New-MgUser -DisplayName $_.DisplayName -UserPrincipalName $_.UserPrincipalName `
               -Department $_.Department -AccountEnabled -PasswordProfile $passwordProfile
}
```

### Создайте политику условного доступа (MFA для администраторов) { #create-a-conditional-access-policy-mfa-for-admins }

```powershell
$adminRoles = (Get-MgDirectoryRole | Where-Object { $_.DisplayName -match "Admin" }).Id
$policy = @{
    DisplayName = "Require MFA for Admins"
    State = "enabledForReportingButNotEnforced"   # Start in report-only mode
    Conditions = @{ Users = @{ IncludeRoles = $adminRoles } }
    GrantControls = @{ Operator = "OR"; BuiltInControls = @("mfa") }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $policy
```

### Связанные генераторы Python { #bundled-python-generators }

Три инструмента stdlib генерируют артефакты PowerShell детерминированным образом — предпочитают их написанию вручную сценариев для массовой / повторяемой работы. Выборочный ввод: `sample_input.json`; ожидаемая форма: `expected_output.json`.

```bash
# Tenant setup: checklist + DNS records + license plan (JSON), or the full setup script
python3 scripts/tenant_setup.py --config sample_input.json --format json -o tenant_plan.json
python3 scripts/tenant_setup.py --config sample_input.json --format powershell -o tenant_setup.ps1

# User lifecycle: validate first, then generate creation/offboarding scripts
python3 scripts/user_management.py --domain acme.com --action validate --users users.json
python3 scripts/user_management.py --domain acme.com --action create --users users.json -o create_users.ps1
python3 scripts/user_management.py --domain acme.com --action offboard --user-email jane@acme.com -o offboard.ps1

# Admin scripts: CA policy / security audit / bulk licensing
python3 scripts/powershell_generator.py --tenant-domain acme.com --task conditional-access --policy-config policy.json -o ca_policy.ps1
python3 scripts/powershell_generator.py --tenant-domain acme.com --task security-audit -o audit.ps1
python3 scripts/powershell_generator.py --tenant-domain acme.com --task bulk-license --users-csv users.csv --license-sku ENTERPRISEPACK -o licenses.ps1
```

**Гейт:** для создания пользователя запустите `--action validate` сначала и требуйте, чтобы каждая запись отчитывалась `"is_valid": true` перед генерацией сценария создания. Ревью каждого сгенерированного `.ps1` сверьтесь с приведенными ниже воркфлоу, прежде чем запускать его в клиенте.

---

## Воркфлоу { #workflows }

### Воркфлоу 1: Настройка нового клиента { #workflow-1-new-tenant-setup }

**Шаг 1: Сгенерируйте Чек-лист настройки.**

Бежать `python3 scripts/tenant_setup.py --config tenant.json --format json` и проработать до конца `setup_checklist` фаза за фазой; `dns_records` подает шаг 2 и `license_recommendations` управляет воркфлоу-процессом лицензирования.

Подтвердите предварительные требования перед подготовкой:
- Учетная запись глобального администратора создана и защищена с помощью MFA
- Пользовательский домен приобретен и доступен для редактирования DNS
- Подтверждены артикулы лицензий (указаны требования к функциям E3 и E5)

**Шаг 2: Настройка и проверка записей DNS**

```powershell
# After adding the domain in the M365 admin center, verify propagation before proceeding
$domain = "company.com"
Resolve-DnsName -Name "_msdcs.$domain" -Type NS -ErrorAction SilentlyContinue
# Also run from a shell prompt:
# nslookup -type=MX company.com
# nslookup -type=TXT company.com   # confirm SPF record
```

Дождитесь распространения DNS (до 48 часов) перед массовым созданием пользователя.

**Шаг 3: Примените базовый уровень безопасности**

```powershell
# Disable legacy authentication (blocks Basic Auth protocols)
$policy = @{
    DisplayName = "Block Legacy Authentication"
    State = "enabled"
    Conditions = @{ ClientAppTypes = @("exchangeActiveSync","other") }
    GrantControls = @{ Operator = "OR"; BuiltInControls = @("block") }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $policy

# Enable unified audit log
Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true
```

**Шаг 4: Подготовка пользователей**

```powershell
$licenseSku = (Get-MgSubscribedSku | Where-Object { $_.SkuPartNumber -eq "ENTERPRISEPACK" }).SkuId

Import-Csv .\employees.csv | ForEach-Object {
    try {
        $user = New-MgUser -DisplayName $_.DisplayName -UserPrincipalName $_.UserPrincipalName `
                           -AccountEnabled -PasswordProfile @{ Password = (New-Guid).ToString().Substring(0,12)+"!"; ForceChangePasswordNextSignIn = $true }
        Set-MgUserLicense -UserId $user.Id -AddLicenses @(@{ SkuId = $licenseSku }) -RemoveLicenses @()
        Write-Host "Provisioned: $($_.UserPrincipalName)"
    } catch {
        Write-Warning "Failed $($_.UserPrincipalName): $_"
    }
}
```

** Проверка:** Выборочно проверьте 3-5 учетных записей на портале администратора M365; подтвердите, что лицензии отображаются как "Активные".

---

### Воркфлоу 2: Усиление безопасности { #workflow-2-security-hardening }

**Шаг 1: Запустите аудит безопасности**

```powershell
Connect-MgGraph -Scopes "Directory.Read.All","Policy.Read.All","AuditLog.Read.All","Reports.Read.All"

# Export Conditional Access policy inventory
Get-MgIdentityConditionalAccessPolicy | Select-Object DisplayName, State |
    Export-Csv .\ca_policies.csv -NoTypeInformation

# Find accounts without MFA registered
$report = Get-MgReportAuthenticationMethodUserRegistrationDetail
$report | Where-Object { -not $_.IsMfaRegistered } |
    Select-Object UserPrincipalName, IsMfaRegistered |
    Export-Csv .\no_mfa_users.csv -NoTypeInformation

Write-Host "Audit complete. Review ca_policies.csv and no_mfa_users.csv."
```

**Шаг 2: Создайте политику МИД (сначала только для отчета)**

```powershell
$policy = @{
    DisplayName = "Require MFA All Users"
    State = "enabledForReportingButNotEnforced"
    Conditions = @{ Users = @{ IncludeUsers = @("All") } }
    GrantControls = @{ Operator = "OR"; BuiltInControls = @("mfa") }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $policy
```

** Проверка:** Через 48 часов ревью логи входа в Entra ID; подтвердите, что ожидаемые пользователи будут оспорены, затем измените `State` к `"enabled"`.

** Шаг 3: Ревью защищенный счет**

```powershell
# Retrieve current Secure Score and top improvement actions
Get-MgSecuritySecureScore -Top 1 | Select-Object CurrentScore, MaxScore, ActiveUserCount
Get-MgSecuritySecureScoreControlProfile | Sort-Object -Property ActionType |
    Select-Object Title, ImplementationStatus, MaxScore | Format-Table -AutoSize
```

---

### Воркфлоу 3: Отключение пользователя { #workflow-3-user-offboarding }

**Шаг 1: Заблокируйте вход в систему и отмените сеансы**

```powershell
$upn = "departing.user@company.com"
$user = Get-MgUser -Filter "userPrincipalName eq '$upn'"

# Block sign-in immediately
Update-MgUser -UserId $user.Id -AccountEnabled:$false

# Revoke all active tokens
Invoke-MgInvalidateAllUserRefreshToken -UserId $user.Id
Write-Host "Sign-in blocked and sessions revoked for $upn"
```

** Шаг 2: Предварительный просмотр с помощью -WhatIf (удаление лицензии)**

```powershell
# Identify assigned licenses
$licenses = (Get-MgUserLicenseDetail -UserId $user.Id).SkuId

# Dry-run: print what would be removed
$licenses | ForEach-Object { Write-Host "[WhatIf] Would remove SKU: $_" }
```

**Шаг 3: Выполните выгрузку**

```powershell
# Remove licenses
Set-MgUserLicense -UserId $user.Id -AddLicenses @() -RemoveLicenses $licenses

# Convert mailbox to shared (requires ExchangeOnlineManagement module)
Set-Mailbox -Identity $upn -Type Shared

# Remove from all groups
Get-MgUserMemberOf -UserId $user.Id | ForEach-Object {
    try { Remove-MgGroupMemberByRef -GroupId $_.Id -DirectoryObjectId $user.Id } catch {}
}
Write-Host "Offboarding complete for $upn"
```

** Проверка: ** Подтвердите на портале администратора M365, что учетная запись отображается как "Заблокированная", у нее нет активных лицензий, а тип почтового ящика - "Общий".

---

## Лучшие практики { #best-practices }

### Настройка арендатора { #tenant-setup }

1. Включите MFA перед добавлением пользователей
2. Настройка именованных местоположений для условного доступа
3. Используйте отдельные учетные записи администратора с PIM
4. Проверьте пользовательские домены (и распространение DNS) перед массовым созданием пользователя
5. Применяйте рекомендации Microsoft Secure Score

### Операции по обеспечению безопасности { #security-operations }

1. Запуск политик условного доступа в режиме только для отчетов
2. Ревью журналы входа в систему в течение 48 часов, прежде чем применять новую политику
3. Никогда не вводите жестко учетные данные в скрипты — используйте хранилище ключей Azure или `Get-Credential`
4. Включить ведение журнала унифицированного аудита для всех операций
5. Проводите ежеквартальные ревью безопасности и безопасные проверки результатов

### Автоматизация PowerShell { #powershell-automation }

1. Предпочитаю Microsoft Graph (`Microsoft.Graph` модуль) поверх устаревшего MSOnline
2. Включать `try/catch` блоки для обработки ошибок
3. Внедрять `Write-Host`/`Write-Warning` ведение журнала для отслеживания результатов аудита
4. Использование `-WhatIf` или выход при сухом прогоне перед массовыми разрушающими операциями
5. Сначала протестируйте в непроизводственном клиенте

---

## Справочные руководства { #reference-guides }

**ссылки/powershell-шаблоны.md**
- Готовые к использованию шаблоны скриптов
- Примеры политики условного доступа
- Сценарии массовой подготовки пользователей
- Сценарии аудита безопасности

**ссылки/security-policies.md**
- Конфигурация условного доступа
- Стратегии правоприменения МИД
- DLP и политика хранения
- Базовые настройки безопасности

**ссылки/устранение неполадок.md**
- Способы устранения распространенных ошибок
- Проблемы с модулем PowerShell
- Устранение неполадок с разрешениями
- Проблемы с распространением DNS

---

## Ограничения { #limitations }

| Ограничение | Воздействие |
|------------|--------|
| Требуется глобальный администратор | Для полной настройки клиента требуются самые высокие привилегии |
| Ограничения скорости API | Массовые операции могут быть ограничены |
| Зависимости от лицензий | E3/E5 требуется для расширенных функций |
| Гибридные сценарии | Локальная реклама нуждается в дополнительной настройке |
| Предварительные требования PowerShell | Майкрософт.Требуется графический модуль |

### Необходимые модули PowerShell { #required-powershell-modules }

```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Install-Module MicrosoftTeams -Scope CurrentUser
```

### Требуемые разрешения { #required-permissions }

- **Глобальный администратор** — Полная настройка клиента
- **Администратор пользователя** — Управление пользователями
- **Администратор безопасности** — Политики безопасности
- **Администратор Exchange** — Управление почтовыми ящиками
