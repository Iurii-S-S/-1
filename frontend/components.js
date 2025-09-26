// Компонент навигационной панели
const NavBarComponent = {
    template: `
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="#" @click="$emit('nav-click', 'dashboard')">
                    <i class="bi bi-clipboard-check"></i> СистемаКонтроля
                </a>
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                        <li class="nav-item">
                            <a class="nav-link" href="#" @click="$emit('nav-click', 'dashboard')" 
                               :class="{ active: $attrs.currentView === 'dashboard' }">
                                <i class="bi bi-speedometer2"></i> Дашборд
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" @click="$emit('nav-click', 'defects')" 
                               :class="{ active: $attrs.currentView === 'defects' }">
                                <i class="bi bi-bug"></i> Дефекты
                            </a>
                        </li>
                        <li v-if="user.role === 'manager'" class="nav-item">
                            <a class="nav-link" href="#" @click="$emit('nav-click', 'projects')" 
                               :class="{ active: $attrs.currentView === 'projects' }">
                                <i class="bi bi-building"></i> Проекты
                            </a>
                        </li>
                        <li v-if="user.role === 'manager'" class="nav-item">
                            <a class="nav-link" href="#" @click="$emit('nav-click', 'reports')" 
                               :class="{ active: $attrs.currentView === 'reports' }">
                                <i class="bi bi-graph-up"></i> Отчеты
                            </a>
                        </li>
                    </ul>
                    
                    <div class="d-flex align-items-center">
                        <span class="navbar-text me-3">
                            {{ user.first_name }} {{ user.last_name }}
                            <span class="badge bg-secondary ms-1">{{ getRoleText(user.role) }}</span>
                        </span>
                        <div class="dropdown">
                            <button class="btn btn-outline-light btn-sm dropdown-toggle" type="button" 
                                    data-bs-toggle="dropdown">
                                <i class="bi bi-person-circle"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li><a class="dropdown-item" href="#" @click="$emit('profile')">
                                    <i class="bi bi-person"></i> Профиль
                                </a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-danger" href="#" @click="$emit('logout')">
                                    <i class="bi bi-box-arrow-right"></i> Выход
                                </a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    `,
    props: ['user'],
    methods: {
        getRoleText(role) {
            const roleMap = {
                'manager': 'Менеджер',
                'engineer': 'Инженер', 
                'observer': 'Наблюдатель'
            };
            return roleMap[role] || role;
        }
    }
};

// Компонент боковой панели
const SideBarComponent = {
    template: `
        <div class="col-lg-2 col-md-3 sidebar">
            <div class="sticky-top" style="top: 80px;">
                <div class="d-flex flex-column gap-3">
                    <!-- Быстрые фильтры -->
                    <div class="card">
                        <div class="card-header bg-transparent">
                            <h6 class="mb-0"><i class="bi bi-funnel"></i> Фильтры</h6>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label class="form-label small">Статус</label>
                                <select class="form-select form-select-sm" v-model="filters.status" @change="applyFilters">
                                    <option value="">Все статусы</option>
                                    <option value="new">Новая</option>
                                    <option value="in_progress">В работе</option>
                                    <option value="review">На проверке</option>
                                    <option value="closed">Закрыта</option>
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label small">Приоритет</label>
                                <select class="form-select form-select-sm" v-model="filters.priority" @change="applyFilters">
                                    <option value="">Все приоритеты</option>
                                    <option value="high">Высокий</option>
                                    <option value="medium">Средний</option>
                                    <option value="low">Низкий</option>
                                </select>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label small">Поиск</label>
                                <input type="text" class="form-control form-control-sm" v-model="filters.search" 
                                       placeholder="Поиск..." @input="onSearchInput">
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button class="btn btn-primary btn-sm" @click="applyFilters">
                                    <i class="bi bi-funnel"></i> Применить
                                </button>
                                <button class="btn btn-outline-secondary btn-sm" @click="resetFilters">
                                    <i class="bi bi-x-circle"></i> Сбросить
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Быстрые действия -->
                    <div class="card">
                        <div class="card-header bg-transparent">
                            <h6 class="mb-0"><i class="bi bi-lightning"></i> Быстрые действия</h6>
                        </div>
                        <div class="card-body">
                            <div class="d-grid gap-2">
                                <button v-if="user.role !== 'observer'" class="btn btn-success btn-sm" 
                                        @click="$emit('create-defect')">
                                    <i class="bi bi-plus-circle"></i> Новый дефект
                                </button>
                                <button v-if="user.role === 'manager'" class="btn btn-info btn-sm" 
                                        @click="$emit('export-data')">
                                    <i class="bi bi-download"></i> Экспорт
                                </button>
                                <button class="btn btn-outline-primary btn-sm" @click="$emit('refresh')">
                                    <i class="bi bi-arrow-clockwise"></i> Обновить
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Статус системы -->
                    <div class="card">
                        <div class="card-header bg-transparent">
                            <h6 class="mb-0"><i class="bi bi-info-circle"></i> Информация</h6>
                        </div>
                        <div class="card-body">
                            <div class="small">
                                <div class="d-flex justify-content-between mb-1">
                                    <span>Дефектов всего:</span>
                                    <span class="badge bg-primary">{{ stats.total || 0 }}</span>
                                </div>
                                <div class="d-flex justify-content-between mb-1">
                                    <span>В работе:</span>
                                    <span class="badge bg-warning">{{ stats.in_progress || 0 }}</span>
                                </div>
                                <div class="d-flex justify-content-between">
                                    <span>Просрочено:</span>
                                    <span class="badge bg-danger">{{ stats.overdue || 0 }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['currentView', 'user', 'stats'],
    data() {
        return {
            filters: {
                status: '',
                priority: '',
                search: ''
            },
            searchTimeout: null
        }
    },
    methods: {
        applyFilters() {
            this.$emit('filter-change', {...this.filters});
        },
        resetFilters() {
            this.filters = {
                status: '',
                priority: '',
                search: ''
            };
            this.applyFilters();
        },
        onSearchInput() {
            // Дебаунс поиска
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                this.applyFilters();
            }, 500);
        }
    }
};

// Компонент модального окна дефекта
const DefectModalComponent = {
    template: `
        <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
            <div class="modal-dialog modal-xl modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            Дефект #{{ defect.id }}: {{ defect.title }}
                        </h5>
                        <button type="button" class="btn-close" @click="$emit('close')"></button>
                    </div>
                    
                    <div class="modal-body">
                        <div class="row">
                            <!-- Основная информация -->
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-header">
                                        <h6 class="mb-0">Основная информация</h6>
                                    </div>
                                    <div class="card-body">
                                        <table class="table table-sm table-borderless">
                                            <tr>
                                                <td width="30%"><strong>Статус:</strong></td>
                                                <td>
                                                    <span class="badge" :class="statusBadgeClass(defect.status)">
                                                        {{ getStatusText(defect.status) }}
                                                    </span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td><strong>Приоритет:</strong></td>
                                                <td>
                                                    <span class="badge" :class="priorityBadgeClass(defect.priority)">
                                                        {{ getPriorityText(defect.priority) }}
                                                    </span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td><strong>Проект:</strong></td>
                                                <td>{{ defect.project_name }}</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Создатель:</strong></td>
                                                <td>{{ defect.creator }}</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Исполнитель:</strong></td>
                                                <td>{{ defect.assignee || 'Не назначен' }}</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Срок:</strong></td>
                                                <td :class="{'text-danger': defect.is_overdue}">
                                                    {{ formatDate(defect.due_date) }}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td><strong>Создан:</strong></td>
                                                <td>{{ formatDateTime(defect.created_at) }}</td>
                                            </tr>
                                            <tr>
                                                <td><strong>Обновлен:</strong></td>
                                                <td>{{ formatDateTime(defect.updated_at) }}</td>
                                            </tr>
                                        </table>
                                    </div>
                                </div>
                                
                                <!-- Управление статусом -->
                                <div v-if="canEditDefect" class="card">
                                    <div class="card-header">
                                        <h6 class="mb-0">Управление статусом</h6>
                                    </div>
                                    <div class="card-body">
                                        <div class="btn-group w-100" role="group">
                                            <button v-for="action in availableActions" :key="action.status"
                                                    class="btn btn-sm" :class="action.class"
                                                    @click="updateStatus(action.status)">
                                                {{ action.label }}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Описание и комментарии -->
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-header">
                                        <h6 class="mb-0">Описание</h6>
                                    </div>
                                    <div class="card-body">
                                        <p class="mb-0">{{ defect.description }}</p>
                                    </div>
                                </div>
                                
                                <!-- Комментарии -->
                                <div class="card">
                                    <div class="card-header d-flex justify-content-between align-items-center">
                                        <h6 class="mb-0">Комментарии ({{ defect.comments_count }})</h6>
                                    </div>
                                    <div class="card-body" style="max-height: 300px; overflow-y: auto;">
                                        <!-- Список комментариев -->
                                        <div v-for="comment in defect.comments" :key="comment.id" 
                                             class="comment mb-3">
                                            <div class="d-flex">
                                                <div class="comment-avatar">
                                                    {{ comment.author.split(' ').map(n => n[0]).join('') }}
                                                </div>
                                                <div class="comment-content">
                                                    <div class="d-flex justify-content-between align-items-start">
                                                        <span class="comment-author">{{ comment.author }}</span>
                                                        <small class="comment-date">{{ formatDateTime(comment.created_at) }}</small>
                                                    </div>
                                                    <div class="comment-role small text-muted">
                                                        {{ getRoleText(comment.author_role) }}
                                                    </div>
                                                    <p class="comment-text mb-0">{{ comment.text }}</p>
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div v-if="defect.comments.length === 0" class="text-center text-muted py-3">
                                            <i class="bi bi-chat-dots"></i><br>
                                            <small>Комментариев пока нет</small>
                                        </div>
                                    </div>
                                    
                                    <!-- Форма добавления комментария -->
                                    <div v-if="user.role !== 'observer'" class="card-footer">
                                        <div class="input-group">
                                            <input type="text" class="form-control form-control-sm" 
                                                   v-model="newComment" placeholder="Добавить комментарий..."
                                                   @keypress.enter="addComment">
                                            <button class="btn btn-primary btn-sm" @click="addComment" 
                                                    :disabled="!newComment.trim()">
                                                <i class="bi bi-send"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" @click="$emit('close')">Закрыть</button>
                        <button v-if="canEditDefect" type="button" class="btn btn-primary" 
                                @click="$emit('edit-defect', defect)">
                            <i class="bi bi-pencil"></i> Редактировать
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['defect', 'user'],
    data() {
        return {
            newComment: ''
        }
    },
    computed: {
        canEditDefect() {
            if (this.user.role === 'manager') return true;
            if (this.user.role === 'engineer' && this.defect.assignee_id === this.user.id) return true;
            return false;
        },
        availableActions() {
            const actions = [];
            const status = this.defect.status;
            
            if (this.user.role === 'manager') {
                if (status === 'new') {
                    actions.push({ status: 'in_progress', label: 'В работу', class: 'btn-warning' });
                    actions.push({ status: 'cancelled', label: 'Отменить', class: 'btn-secondary' });
                }
                if (status === 'review') {
                    actions.push({ status: 'closed', label: 'Закрыть', class: 'btn-success' });
                    actions.push({ status: 'in_progress', label: 'На доработку', class: 'btn-warning' });
                }
            }
            
            if (this.user.role === 'engineer' && this.defect.assignee_id === this.user.id) {
                if (status === 'in_progress') {
                    actions.push({ status: 'review', label: 'На проверку', class: 'btn-info' });
                }
            }
            
            return actions;
        }
    },
    methods: {
        getStatusText(status) {
            const statusMap = {
                'new': 'Новая', 'in_progress': 'В работе', 
                'review': 'На проверке', 'closed': 'Закрыта', 'cancelled': 'Отменена'
            };
            return statusMap[status] || status;
        },
        
        getPriorityText(priority) {
            const priorityMap = {
                'high': 'Высокий', 'medium': 'Средний', 'low': 'Низкий'
            };
            return priorityMap[priority] || priority;
        },
        
        getRoleText(role) {
            const roleMap = {
                'manager': 'Менеджер', 'engineer': 'Инженер', 'observer': 'Наблюдатель'
            };
            return roleMap[role] || role;
        },
        
        statusBadgeClass(status) {
            const classes = {
                'new': 'bg-secondary',
                'in_progress': 'bg-warning',
                'review': 'bg-info', 
                'closed': 'bg-success',
                'cancelled': 'bg-danger'
            };
            return classes[status] || 'bg-secondary';
        },
        
        priorityBadgeClass(priority) {
            const classes = {
                'high': 'bg-danger',
                'medium': 'bg-warning',
                'low': 'bg-success'
            };
            return classes[priority] || 'bg-secondary';
        },
        
        formatDate(dateString) {
            if (!dateString) return 'Не указан';
            return new Date(dateString).toLocaleDateString('ru-RU');
        },
        
        formatDateTime(dateString) {
            if (!dateString) return '';
            return new Date(dateString).toLocaleString('ru-RU');
        },
        
        async updateStatus(newStatus) {
            try {
                const response = await axios.put(`/api/v1/defects/${this.defect.id}`, {
                    status: newStatus
                });
                
                if (response.data.success) {
                    this.$emit('defect-updated');
                    this.$emit('close');
                }
            } catch (error) {
                console.error('Ошибка обновления статуса:', error);
                alert('Ошибка при обновлении статуса');
            }
        },
        
        async addComment() {
            if (!this.newComment.trim()) return;
            
            try {
                const response = await axios.post(`/api/v1/defects/${this.defect.id}/comments`, {
                    text: this.newComment
                });
                
                if (response.data.success) {
                    this.defect.comments.push(response.data.comment);
                    this.defect.comments_count++;
                    this.newComment = '';
                }
            } catch (error) {
                console.error('Ошибка добавления комментария:', error);
                alert('Ошибка при добавлении комментария');
            }
        }
    }
};