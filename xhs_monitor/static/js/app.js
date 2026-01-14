// 应用程序主要JavaScript文件
let currentDetailNoteId = null;
let allContents = [];
let allAccounts = [];
let typeChart = null;
let statusChart = null;

// 初始化应用
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadAccounts();
    loadStatistics();
    loadContents();
    
    // 定时刷新统计数据
    setInterval(loadStatistics, 30000);
});

// 初始化应用
function initializeApp() {
    console.log('应用初始化...');
}

// 设置事件监听器
function setupEventListeners() {
    // 账号管理
    document.getElementById('addAccountForm').addEventListener('submit', handleAddAccount);
    
    // 内容爬取
    document.getElementById('fetchContentBtn').addEventListener('click', handleFetchContent);
    document.getElementById('filterBtn').addEventListener('click', handleFilterContents);
    
    // 转换按钮
    document.getElementById('convertContentBtn').addEventListener('click', handleConvertContent);
    
    // 导航链接
    document.querySelectorAll('.navbar-nav a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.getAttribute('href').substring(1);
            showSection(section);
        });
    });
}

// 显示指定部分
function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
    
    // 重新初始化图表
    if (sectionId === 'dashboard') {
        setTimeout(() => {
            if (typeChart) typeChart.resize();
            if (statusChart) statusChart.resize();
        }, 100);
    }
}

// ==================== 账号管理 ====================

// 加载账号列表
async function loadAccounts() {
    try {
        showLoading(true);
        const response = await fetch('/api/accounts');
        const result = await response.json();
        
        if (result.code === 0) {
            allAccounts = result.data;
            renderAccountsTable();
            updateAccountSelects();
        } else {
            showError(result.message);
        }
    } catch (error) {
        showError('加载账号失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 渲染账号表格
function renderAccountsTable() {
    const tbody = document.getElementById('accountsTableBody');
    tbody.innerHTML = '';
    
    if (allAccounts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">暂无账号</td></tr>';
        return;
    }
    
    allAccounts.forEach(account => {
        const row = document.createElement('tr');
        const createdAt = new Date(account.created_at).toLocaleDateString('zh-CN');
        
        row.innerHTML = `
            <td><strong>${escapeHtml(account.username)}</strong></td>
            <td><code>${escapeHtml(account.user_id)}</code></td>
            <td>${createdAt}</td>
            <td>
                <span class="badge badge-success">${account.status}</span>
            </td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="handleDeleteAccount('${account.account_id}')">
                    <i class="bi bi-trash"></i> 删除
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// 添加账号
async function handleAddAccount(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const userId = document.getElementById('userId').value.trim();
    const cookie = document.getElementById('cookie').value.trim();
    const a1 = document.getElementById('a1').value.trim();
    
    if (!username || !userId || !cookie) {
        showError('请填写所有必填字段');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch('/api/accounts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username,
                user_id: userId,
                cookie,
                a1
            })
        });
        
        const result = await response.json();
        
        if (result.code === 0) {
            showSuccess('账号添加成功');
            document.getElementById('addAccountForm').reset();
            loadAccounts();
        } else {
            showError(result.message);
        }
    } catch (error) {
        showError('添加账号失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 删除账号
async function handleDeleteAccount(accountId) {
    if (!confirm('确认删除该账号吗？')) return;
    
    try {
        showLoading(true);
        const response = await fetch(`/api/accounts/${accountId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.code === 0) {
            showSuccess('账号删除成功');
            loadAccounts();
        } else {
            showError(result.message);
        }
    } catch (error) {
        showError('删除账号失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 更新账号选择框
function updateAccountSelects() {
    const fetchSelect = document.getElementById('fetchAccountSelect');
    const filterSelect = document.getElementById('filterUserSelect');
    
    fetchSelect.innerHTML = '<option value="">-- 选择账号 --</option>';
    const users = new Set();
    
    allAccounts.forEach(account => {
        const option = document.createElement('option');
        option.value = account.account_id;
        option.textContent = `${account.username} (${account.user_id})`;
        fetchSelect.appendChild(option);
        users.add(account.user_id);
    });
    
    // 获取所有不同的用户ID
    filterSelect.innerHTML = '<option value="">-- 所有用户 --</option>';
    allContents.forEach(content => {
        users.add(content.user_id);
    });
    users.forEach(userId => {
        const option = document.createElement('option');
        option.value = userId;
        option.textContent = userId;
        filterSelect.appendChild(option);
    });
}

// ==================== 内容管理 ====================

// 爬取内容
async function handleFetchContent() {
    const accountId = document.getElementById('fetchAccountSelect').value;
    const userId = document.getElementById('fetchUserId').value.trim();
    
    if (!accountId) {
        showError('请选择一个账号');
        return;
    }
    
    if (!userId) {
        showError('请输入目标用户ID');
        return;
    }
    
    if (userId.length < 3) {
        showError('用户ID格式不正确（太短）');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch('/api/fetch-content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                account_id: accountId,
                user_id: userId
            })
        });
        
        const result = await response.json();
        
        if (result.code === 0) {
            const message = result.message || '爬取完成';
            showSuccess(message);
            document.getElementById('fetchUserId').value = '';
            
            // 刷新数据
            setTimeout(() => {
                loadContents();
                loadStatistics();
            }, 500);
        } else {
            const errMsg = result.message || '爬取失败';
            showError(errMsg);
            
            // 显示诊断信息
            console.error('爬取错误详情:', result);
        }
    } catch (error) {
        showError('爬取内容失败: ' + error.message);
        console.error('爬取异常:', error);
    } finally {
        showLoading(false);
    }
}

// 加载内容
async function loadContents() {
    try {
        showLoading(true);
        const response = await fetch('/api/contents/user/all?limit=1000');
        
        // 如果没有这个接口，则从其他地方获取
        const allContentsResponse = await fetch('/api/statistics');
        if (allContentsResponse.ok) {
            // 获取统计数据后，手动加载所有内容
            loadAllContentsData();
        }
    } catch (error) {
        console.error('加载内容失败:', error);
    } finally {
        showLoading(false);
    }
}

// 加载所有内容数据
function loadAllContentsData() {
    // 这里需要通过其他方式获取所有内容
    // 由于后端没有提供获取所有内容的接口，我们可以从本地存储或通过其他方式获取
}

// 筛选内容
async function handleFilterContents() {
    const userId = document.getElementById('filterUserSelect').value;
    const contentType = document.getElementById('filterTypeSelect').value;
    const status = document.getElementById('filterStatusSelect').value;
    
    let filteredContents = allContents;
    
    if (userId) {
        filteredContents = filteredContents.filter(c => c.user_id === userId);
    }
    
    if (contentType) {
        filteredContents = filteredContents.filter(c => c.content_type === contentType);
    }
    
    if (status) {
        filteredContents = filteredContents.filter(c => c.conversion_status === status);
    }
    
    renderContentsList(filteredContents);
    showSuccess(`筛选结果: ${filteredContents.length} 条内容`);
}

// 渲染内容列表
function renderContentsList(contents) {
    const container = document.getElementById('contentsContainer');
    
    if (contents.length === 0) {
        container.innerHTML = '<div class="alert alert-info text-center">暂无内容</div>';
        return;
    }
    
    container.innerHTML = contents.map(content => {
        const publishTime = new Date(content.publish_time * 1000).toLocaleDateString('zh-CN');
        const contentTypeLabel = getContentTypeLabel(content.content_type);
        const statusLabel = getStatusLabel(content.conversion_status);
        
        return `
            <div class="content-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div style="flex: 1;">
                        <div class="content-title" onclick="showContentDetail('${content.note_id}')">
                            ${escapeHtml(content.title || '未命名内容')}
                        </div>
                        <div class="content-meta">
                            <span class="text-muted"><i class="bi bi-calendar"></i> ${publishTime}</span>
                            <span class="text-muted ms-3"><i class="bi bi-person"></i> ${escapeHtml(content.username)}</span>
                        </div>
                        <div class="mt-2">
                            <span class="content-tag tag-${content.content_type}">${contentTypeLabel}</span>
                            <span class="content-tag tag-${content.conversion_status}">${statusLabel}</span>
                        </div>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-info" onclick="showContentDetail('${content.note_id}')">
                            <i class="bi bi-eye"></i> 查看
                        </button>
                    </div>
                </div>
                <div class="mt-3">
                    <a href="${escapeHtml(content.link)}" target="_blank" class="content-link">
                        <i class="bi bi-link-45deg"></i> 原始链接
                    </a>
                </div>
                ${content.converted_text ? `
                    <div class="conversion-text">
                        ${escapeHtml(content.converted_text.substring(0, 200))}${content.converted_text.length > 200 ? '...' : ''}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

// 显示内容详情
async function showContentDetail(noteId) {
    try {
        showLoading(true);
        const response = await fetch(`/api/contents/${noteId}`);
        const result = await response.json();
        
        if (result.code === 0) {
            const content = result.data;
            currentDetailNoteId = noteId;
            
            const modalTitle = document.getElementById('contentTitle');
            const modalBody = document.getElementById('contentDetailBody');
            
            modalTitle.textContent = escapeHtml(content.title || '内容详情');
            
            const publishTime = new Date(content.publish_time * 1000).toLocaleString('zh-CN');
            
            let mediaHtml = '';
            if (content.img_urls && content.img_urls.length > 0) {
                mediaHtml = `
                    <div class="mt-3">
                        <h6>图片</h6>
                        <div>
                            ${content.img_urls.map(url => 
                                `<img src="${escapeHtml(url)}" class="img-thumbnail-small" alt="内容图片" onerror="this.style.display='none'">`
                            ).join('')}
                        </div>
                    </div>
                `;
            }
            
            if (content.video_url) {
                mediaHtml += `
                    <div class="mt-3">
                        <h6>视频</h6>
                        <a href="${escapeHtml(content.video_url)}" target="_blank" class="content-link">
                            <i class="bi bi-play-circle"></i> 查看视频
                        </a>
                    </div>
                `;
            }
            
            modalBody.innerHTML = `
                <div class="row mb-3">
                    <div class="col-md-6">
                        <strong>发布时间:</strong> ${publishTime}
                    </div>
                    <div class="col-md-6">
                        <strong>内容类型:</strong>
                        <span class="content-tag tag-${content.content_type}">${getContentTypeLabel(content.content_type)}</span>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <strong>博主:</strong> ${escapeHtml(content.username)}
                    </div>
                    <div class="col-md-6">
                        <strong>转换状态:</strong>
                        <span class="content-tag tag-${content.conversion_status}">${getStatusLabel(content.conversion_status)}</span>
                    </div>
                </div>
                
                <div class="mb-3">
                    <strong>原始描述:</strong>
                    <div class="conversion-text" style="border-left-color: #1890ff; background-color: #f0f5ff;">
                        ${escapeHtml(content.desc || '（无描述）')}
                    </div>
                </div>
                
                ${mediaHtml}
                
                ${content.converted_text ? `
                    <div class="mb-3">
                        <strong>转换后的文本:</strong>
                        <div class="conversion-text">
                            ${escapeHtml(content.converted_text)}
                        </div>
                    </div>
                ` : `
                    <div class="alert alert-warning">
                        <i class="bi bi-exclamation-triangle"></i> 还未转换
                    </div>
                `}
                
                <div class="mt-3">
                    <a href="${escapeHtml(content.link)}" target="_blank" class="btn btn-primary btn-sm">
                        <i class="bi bi-link-45deg"></i> 访问原始链接
                    </a>
                </div>
            `;
            
            const modal = new bootstrap.Modal(document.getElementById('contentDetailModal'));
            modal.show();
        }
    } catch (error) {
        showError('加载内容详情失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// 转换单条内容
async function handleConvertContent() {
    if (!currentDetailNoteId) return;
    
    try {
        showLoading(true);
        const response = await fetch(`/api/convert-content/${currentDetailNoteId}`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.code === 0) {
            showSuccess('转换成功');
            // 更新本地数据
            const content = result.data;
            const index = allContents.findIndex(c => c.note_id === currentDetailNoteId);
            if (index !== -1) {
                allContents[index] = content;
            }
            // 重新显示详情
            showContentDetail(currentDetailNoteId);
            loadStatistics();
        } else {
            showError(result.message);
        }
    } catch (error) {
        showError('转换失败: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// ==================== 统计信息 ====================

// 加载统计数据
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const result = await response.json();
        
        if (result.code === 0) {
            const stats = result.data;
            
            // 更新统计卡片
            document.getElementById('stat-accounts').textContent = stats.total_accounts;
            document.getElementById('stat-contents').textContent = stats.total_contents;
            document.getElementById('stat-converted').textContent = stats.conversion_status.completed;
            document.getElementById('stat-pending').textContent = stats.conversion_status.pending;
            
            // 更新图表
            updateCharts(stats);
        }
    } catch (error) {
        console.error('加载统计数据失败:', error);
    }
}

// 更新图表
function updateCharts(stats) {
    const typeCtx = document.getElementById('typeChart');
    const statusCtx = document.getElementById('statusChart');
    
    // 内容类型图表
    if (typeChart) {
        typeChart.destroy();
    }
    typeChart = new Chart(typeCtx, {
        type: 'doughnut',
        data: {
            labels: ['视频', '图片', '文字'],
            datasets: [{
                data: [
                    stats.content_types.video,
                    stats.content_types.image,
                    stats.content_types.text
                ],
                backgroundColor: ['#1890ff', '#52c41a', '#faad14']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // 转换状态图表
    if (statusChart) {
        statusChart.destroy();
    }
    statusChart = new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['已转换', '待转换', '失败'],
            datasets: [{
                data: [
                    stats.conversion_status.completed,
                    stats.conversion_status.pending,
                    stats.conversion_status.failed
                ],
                backgroundColor: ['#52c41a', '#faad14', '#f5222d']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// ==================== 辅助函数 ====================

// 获取内容类型标签
function getContentTypeLabel(type) {
    const labels = {
        'video': '📹 视频',
        'image': '🖼️ 图片',
        'text': '📝 文字'
    };
    return labels[type] || '未知';
}

// 获取转换状态标签
function getStatusLabel(status) {
    const labels = {
        'completed': '✓ 已转换',
        'pending': '○ 待转换',
        'processing': '⊙ 转换中',
        'failed': '✕ 失败'
    };
    return labels[status] || '未知';
}

// 显示加载状态
function showLoading(show) {
    document.getElementById('loadingSpinner').style.display = show ? 'flex' : 'none';
}

// 显示成功消息
function showSuccess(message) {
    showAlert(message, 'success');
}

// 显示错误消息
function showError(message) {
    showAlert(message, 'danger');
}

// 显示警告消息
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9998';
    alertDiv.style.maxWidth = '400px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 3秒后自动移除
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
