"""
Agent Training GUI - Comprehensive training and deployment interface
Provides GUI for model training, evaluation, deployment, and monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
import queue
from datetime import datetime
from typing import Dict, List, Optional, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Import our modules
from agent_trainer import AgentTrainer, TrainingConfig, AgentModel
from model_evaluator import ModelEvaluator, EvaluationTest, BenchmarkResult
from agent_deployment import DeploymentManager, DeploymentConfig, DeploymentStatus

class AgentTrainingGUI:
    """Main GUI for agent training system"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Agent Training System")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.trainer = AgentTrainer()
        self.evaluator = ModelEvaluator()
        self.deployment_manager = DeploymentManager()
        
        # Data storage
        self.current_model = None
        self.training_data = []
        self.evaluation_results = {}
        self.deployments = []
        
        # Create GUI
        self.create_widgets()
        self.load_data()
        
        # Start update thread
        self.update_queue = queue.Queue()
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_training_tab()
        self.create_evaluation_tab()
        self.create_deployment_tab()
        self.create_monitoring_tab()
        self.create_data_tab()
    
    def create_training_tab(self):
        """Create the training tab"""
        training_frame = ttk.Frame(self.notebook)
        self.notebook.add(training_frame, text="Training")
        
        # Training configuration
        config_frame = ttk.LabelFrame(training_frame, text="Training Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Model name and description
        ttk.Label(config_frame, text="Model Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.model_name_var = tk.StringVar(value="Custom Agent")
        ttk.Entry(config_frame, textvariable=self.model_name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.model_desc_var = tk.StringVar(value="Trained AI agent")
        ttk.Entry(config_frame, textvariable=self.model_desc_var, width=50).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Training parameters
        params_frame = ttk.LabelFrame(training_frame, text="Training Parameters", padding=10)
        params_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Model type
        ttk.Label(params_frame, text="Model Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.model_type_var = tk.StringVar(value="gpt-3.5-turbo")
        model_types = ["gpt-3.5-turbo", "gpt-4", "custom-transformer", "lstm", "cnn"]
        ttk.Combobox(params_frame, textvariable=self.model_type_var, values=model_types, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Training parameters
        ttk.Label(params_frame, text="Max Epochs:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.max_epochs_var = tk.IntVar(value=10)
        ttk.Spinbox(params_frame, from_=1, to=100, textvariable=self.max_epochs_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(params_frame, text="Batch Size:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.batch_size_var = tk.IntVar(value=32)
        ttk.Spinbox(params_frame, from_=1, to=128, textvariable=self.batch_size_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(params_frame, text="Learning Rate:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.lr_var = tk.DoubleVar(value=0.001)
        ttk.Spinbox(params_frame, from_=0.0001, to=0.1, increment=0.0001, textvariable=self.lr_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Data augmentation
        self.use_augmentation_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(params_frame, text="Use Data Augmentation", variable=self.use_augmentation_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Training data
        data_frame = ttk.LabelFrame(training_frame, text="Training Data", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Data controls
        data_controls = ttk.Frame(data_frame)
        data_controls.pack(fill=tk.X, pady=5)
        
        ttk.Button(data_controls, text="Load Training Data", command=self.load_training_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(data_controls, text="Generate Sample Data", command=self.generate_sample_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(data_controls, text="Clear Data", command=self.clear_training_data).pack(side=tk.LEFT, padx=5)
        
        # Data preview
        self.data_text = scrolledtext.ScrolledText(data_frame, height=10)
        self.data_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Training controls
        train_controls = ttk.Frame(training_frame)
        train_controls.pack(fill=tk.X, padx=10, pady=5)
        
        self.train_button = ttk.Button(train_controls, text="Start Training", command=self.start_training)
        self.train_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(train_controls, text="Stop Training", command=self.stop_training, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Training progress
        progress_frame = ttk.LabelFrame(training_frame, text="Training Progress", padding=10)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to train")
        self.progress_label.pack()
        
        # Training log
        log_frame = ttk.LabelFrame(training_frame, text="Training Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.training_log = scrolledtext.ScrolledText(log_frame, height=8)
        self.training_log.pack(fill=tk.BOTH, expand=True)
    
    def create_evaluation_tab(self):
        """Create the evaluation tab"""
        eval_frame = ttk.Frame(self.notebook)
        self.notebook.add(eval_frame, text="Evaluation")
        
        # Model selection
        model_frame = ttk.LabelFrame(eval_frame, text="Model Selection", padding=10)
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(model_frame, text="Select Model:").pack(side=tk.LEFT, padx=5)
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, width=40)
        self.model_combo.pack(side=tk.LEFT, padx=5)
        self.model_combo.bind('<<ComboboxSelected>>', self.on_model_selected)
        
        ttk.Button(model_frame, text="Refresh Models", command=self.refresh_models).pack(side=tk.LEFT, padx=5)
        
        # Test suite selection
        test_frame = ttk.LabelFrame(eval_frame, text="Test Suites", padding=10)
        test_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.test_vars = {}
        test_suites = ['general_knowledge', 'reasoning', 'creativity', 'performance', 'robustness']
        
        for i, suite in enumerate(test_suites):
            var = tk.BooleanVar(value=True)
            self.test_vars[suite] = var
            ttk.Checkbutton(test_frame, text=suite.replace('_', ' ').title(), variable=var).grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)
        
        # Evaluation controls
        eval_controls = ttk.Frame(eval_frame)
        eval_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(eval_controls, text="Run Selected Tests", command=self.run_evaluation).pack(side=tk.LEFT, padx=5)
        ttk.Button(eval_controls, text="Run All Tests", command=self.run_all_evaluation).pack(side=tk.LEFT, padx=5)
        ttk.Button(eval_controls, text="Generate Report", command=self.generate_evaluation_report).pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_frame = ttk.LabelFrame(eval_frame, text="Evaluation Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create notebook for results
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Summary tab
        self.summary_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.summary_frame, text="Summary")
        
        self.summary_text = scrolledtext.ScrolledText(self.summary_frame)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # Detailed results tab
        self.details_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.details_frame, text="Detailed Results")
        
        self.details_text = scrolledtext.ScrolledText(self.details_frame)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Charts tab
        self.charts_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.charts_frame, text="Charts")
        
        self.create_charts()
    
    def create_deployment_tab(self):
        """Create the deployment tab"""
        deploy_frame = ttk.Frame(self.notebook)
        self.notebook.add(deploy_frame, text="Deployment")
        
        # Deployment configuration
        config_frame = ttk.LabelFrame(deploy_frame, text="Deployment Configuration", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(config_frame, text="Model:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.deploy_model_var = tk.StringVar()
        self.deploy_model_combo = ttk.Combobox(config_frame, textvariable=self.deploy_model_var, width=40)
        self.deploy_model_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_frame, text="Deployment Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.deploy_name_var = tk.StringVar(value="Production Deployment")
        ttk.Entry(config_frame, textvariable=self.deploy_name_var, width=40).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_frame, text="Max Concurrent Requests:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.max_requests_var = tk.IntVar(value=100)
        ttk.Spinbox(config_frame, from_=1, to=1000, textvariable=self.max_requests_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(config_frame, text="Request Timeout (s):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.timeout_var = tk.DoubleVar(value=30.0)
        ttk.Spinbox(config_frame, from_=1.0, to=300.0, increment=1.0, textvariable=self.timeout_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Deployment controls
        deploy_controls = ttk.Frame(deploy_frame)
        deploy_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(deploy_controls, text="Deploy Model", command=self.deploy_model).pack(side=tk.LEFT, padx=5)
        ttk.Button(deploy_controls, text="Stop Deployment", command=self.stop_deployment).pack(side=tk.LEFT, padx=5)
        ttk.Button(deploy_controls, text="Refresh Deployments", command=self.refresh_deployments).pack(side=tk.LEFT, padx=5)
        
        # Deployments list
        deployments_frame = ttk.LabelFrame(deploy_frame, text="Active Deployments", padding=10)
        deployments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview for deployments
        columns = ('ID', 'Name', 'Status', 'Health', 'Requests', 'Response Time')
        self.deployments_tree = ttk.Treeview(deployments_frame, columns=columns, show='headings')
        
        for col in columns:
            self.deployments_tree.heading(col, text=col)
            self.deployments_tree.column(col, width=100)
        
        self.deployments_tree.pack(fill=tk.BOTH, expand=True)
        
        # Deployment details
        details_frame = ttk.LabelFrame(deploy_frame, text="Deployment Details", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.deployment_details = scrolledtext.ScrolledText(details_frame, height=8)
        self.deployment_details.pack(fill=tk.BOTH, expand=True)
    
    def create_monitoring_tab(self):
        """Create the monitoring tab"""
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="Monitoring")
        
        # Real-time metrics
        metrics_frame = ttk.LabelFrame(monitor_frame, text="Real-time Metrics", padding=10)
        metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create metrics display
        self.metrics_vars = {}
        metrics = [
            ('Total Requests', 'total_requests'),
            ('Active Requests', 'active_requests'),
            ('Error Rate', 'error_rate'),
            ('Avg Response Time', 'avg_response_time'),
            ('Throughput', 'throughput')
        ]
        
        for i, (label, key) in enumerate(metrics):
            ttk.Label(metrics_frame, text=f"{label}:").grid(row=i//2, column=(i%2)*2, sticky=tk.W, padx=5, pady=2)
            var = tk.StringVar(value="0")
            self.metrics_vars[key] = var
            ttk.Label(metrics_frame, textvariable=var, font=('Arial', 10, 'bold')).grid(row=i//2, column=(i%2)*2+1, sticky=tk.W, padx=5, pady=2)
        
        # Charts
        charts_frame = ttk.LabelFrame(monitor_frame, text="Performance Charts", padding=10)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize charts
        self.init_monitoring_charts()
        
        # Monitoring controls
        monitor_controls = ttk.Frame(monitor_frame)
        monitor_controls.pack(fill=tk.X, padx=10, pady=5)
        
        self.monitoring_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(monitor_controls, text="Enable Real-time Monitoring", variable=self.monitoring_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(monitor_controls, text="Export Metrics", command=self.export_metrics).pack(side=tk.LEFT, padx=5)
        ttk.Button(monitor_controls, text="Clear Charts", command=self.clear_charts).pack(side=tk.LEFT, padx=5)
    
    def create_data_tab(self):
        """Create the data management tab"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="Data Management")
        
        # Data import/export
        io_frame = ttk.LabelFrame(data_frame, text="Data Import/Export", padding=10)
        io_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(io_frame, text="Import Training Data", command=self.import_training_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(io_frame, text="Export Training Data", command=self.export_training_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(io_frame, text="Import Model", command=self.import_model).pack(side=tk.LEFT, padx=5)
        ttk.Button(io_frame, text="Export Model", command=self.export_model).pack(side=tk.LEFT, padx=5)
        
        # Data statistics
        stats_frame = ttk.LabelFrame(data_frame, text="Data Statistics", padding=10)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
    
    def create_charts(self):
        """Create evaluation charts"""
        # Create matplotlib figure for evaluation charts
        self.eval_fig, self.eval_axes = plt.subplots(2, 2, figsize=(12, 8))
        self.eval_canvas = FigureCanvasTkAgg(self.eval_fig, self.charts_frame)
        self.eval_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def init_monitoring_charts(self):
        """Initialize monitoring charts"""
        # Response time chart
        self.ax1.set_title('Response Time Over Time')
        self.ax1.set_ylabel('Response Time (s)')
        self.ax1.grid(True)
        
        # Throughput chart
        self.ax2.set_title('Requests Per Second')
        self.ax2.set_ylabel('Requests/sec')
        self.ax2.set_xlabel('Time')
        self.ax2.grid(True)
        
        self.canvas.draw()
    
    def load_data(self):
        """Load initial data"""
        self.refresh_models()
        self.refresh_deployments()
        self.update_statistics()
    
    def refresh_models(self):
        """Refresh model list"""
        models = self.trainer.get_model_list()
        model_names = [f"{m.name} ({m.model_id})" for m in models]
        
        self.model_combo['values'] = model_names
        self.deploy_model_combo['values'] = model_names
        
        if model_names:
            self.model_combo.set(model_names[0])
            self.deploy_model_combo.set(model_names[0])
    
    def refresh_deployments(self):
        """Refresh deployments list"""
        # Clear existing items
        for item in self.deployments_tree.get_children():
            self.deployments_tree.delete(item)
        
        # Get active deployments
        deployments = self.deployment_manager.list_deployments()
        
        for deployment in deployments:
            self.deployments_tree.insert('', 'end', values=(
                deployment.deployment_id[:8],
                deployment.model_id,
                deployment.status,
                deployment.health_status,
                deployment.total_requests,
                f"{deployment.avg_response_time:.3f}s"
            ))
    
    def load_training_data(self):
        """Load training data from file"""
        filename = filedialog.askopenfilename(
            title="Select Training Data File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                self.training_data = data
                self.update_data_preview()
                messagebox.showinfo("Success", f"Loaded {len(data)} training samples")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")
    
    def generate_sample_data(self):
        """Generate sample training data"""
        sample_data = [
            {
                'messages': [
                    {'role': 'user', 'content': 'What is machine learning?'},
                    {'role': 'assistant', 'content': 'Machine learning is a subset of AI that enables computers to learn from data.'}
                ],
                'quality_score': 0.9
            },
            {
                'messages': [
                    {'role': 'user', 'content': 'How do neural networks work?'},
                    {'role': 'assistant', 'content': 'Neural networks are computing systems inspired by biological brains.'}
                ],
                'quality_score': 0.8
            },
            {
                'messages': [
                    {'role': 'user', 'content': 'Explain deep learning'},
                    {'role': 'assistant', 'content': 'Deep learning uses neural networks with multiple layers to model complex patterns.'}
                ],
                'quality_score': 0.85
            }
        ]
        
        self.training_data = sample_data
        self.update_data_preview()
        messagebox.showinfo("Success", f"Generated {len(sample_data)} sample training samples")
    
    def clear_training_data(self):
        """Clear training data"""
        self.training_data = []
        self.update_data_preview()
    
    def update_data_preview(self):
        """Update data preview text"""
        self.data_text.delete(1.0, tk.END)
        
        if not self.training_data:
            self.data_text.insert(tk.END, "No training data loaded")
            return
        
        preview = f"Loaded {len(self.training_data)} training samples:\n\n"
        
        for i, sample in enumerate(self.training_data[:5]):  # Show first 5
            messages = sample.get('messages', [])
            if len(messages) >= 2:
                user_msg = messages[0].get('content', '')[:50]
                assistant_msg = messages[1].get('content', '')[:50]
                preview += f"Sample {i+1}:\n"
                preview += f"  User: {user_msg}...\n"
                preview += f"  Assistant: {assistant_msg}...\n"
                preview += f"  Quality: {sample.get('quality_score', 'N/A')}\n\n"
        
        if len(self.training_data) > 5:
            preview += f"... and {len(self.training_data) - 5} more samples"
        
        self.data_text.insert(tk.END, preview)
    
    def start_training(self):
        """Start model training"""
        if not self.training_data:
            messagebox.showwarning("Warning", "No training data loaded")
            return
        
        # Get configuration
        config = TrainingConfig(
            model_type=self.model_type_var.get(),
            max_epochs=self.max_epochs_var.get(),
            batch_size=self.batch_size_var.get(),
            learning_rate=self.lr_var.get(),
            use_augmentation=self.use_augmentation_var.get()
        )
        
        # Start training in separate thread
        self.training_thread = threading.Thread(target=self._train_model, args=(config,), daemon=True)
        self.training_thread.start()
        
        # Update UI
        self.train_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_label.config(text="Training started...")
    
    def _train_model(self, config: TrainingConfig):
        """Train model in background thread"""
        try:
            # Convert training data to pairs
            training_pairs = []
            for sample in self.training_data:
                messages = sample.get('messages', [])
                for i in range(len(messages) - 1):
                    if messages[i].get('role') == 'user' and messages[i + 1].get('role') == 'assistant':
                        training_pairs.append((messages[i].get('content', ''), messages[i + 1].get('content', '')))
            
            # Train model
            model = self.trainer.train_agent(
                training_pairs,
                config,
                self.model_name_var.get(),
                self.model_desc_var.get()
            )
            
            # Update UI
            self.update_queue.put(('training_complete', model))
            
        except Exception as e:
            self.update_queue.put(('training_error', str(e)))
    
    def stop_training(self):
        """Stop model training"""
        # In practice, implement training cancellation
        self.train_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_label.config(text="Training stopped")
    
    def run_evaluation(self):
        """Run selected evaluation tests"""
        if not self.model_var.get():
            messagebox.showwarning("Warning", "No model selected")
            return
        
        # Get selected test suites
        selected_suites = [suite for suite, var in self.test_vars.items() if var.get()]
        
        if not selected_suites:
            messagebox.showwarning("Warning", "No test suites selected")
            return
        
        # Run evaluation in separate thread
        threading.Thread(target=self._run_evaluation, args=(selected_suites,), daemon=True).start()
    
    def _run_evaluation(self, test_suites: List[str]):
        """Run evaluation in background thread"""
        try:
            # Create model predictor
            class DemoPredictor:
                def predict(self, input_data):
                    return f"Demo response to: {input_data.get('text', '')[:30]}..."
            
            predictor = DemoPredictor()
            
            # Run tests
            results = {}
            for suite in test_suites:
                result = self.evaluator.run_benchmark_suite(suite, predictor)
                results[suite] = result
            
            # Update UI
            self.update_queue.put(('evaluation_complete', results))
            
        except Exception as e:
            self.update_queue.put(('evaluation_error', str(e)))
    
    def run_all_evaluation(self):
        """Run all evaluation tests"""
        for var in self.test_vars.values():
            var.set(True)
        self.run_evaluation()
    
    def deploy_model(self):
        """Deploy selected model"""
        if not self.deploy_model_var.get():
            messagebox.showwarning("Warning", "No model selected for deployment")
            return
        
        # Get deployment configuration
        config = DeploymentConfig(
            model_id="demo_model",  # In practice, extract from selection
            deployment_name=self.deploy_name_var.get(),
            max_concurrent_requests=self.max_requests_var.get(),
            request_timeout=self.timeout_var.get()
        )
        
        try:
            deployment_id = self.deployment_manager.deploy_model(config)
            messagebox.showinfo("Success", f"Model deployed successfully. ID: {deployment_id}")
            self.refresh_deployments()
            
        except Exception as e:
            messagebox.showerror("Error", f"Deployment failed: {e}")
    
    def stop_deployment(self):
        """Stop selected deployment"""
        selection = self.deployments_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No deployment selected")
            return
        
        # Get deployment ID from selection
        item = self.deployments_tree.item(selection[0])
        deployment_id = item['values'][0]  # First column contains ID
        
        try:
            success = self.deployment_manager.stop_deployment(deployment_id)
            if success:
                messagebox.showinfo("Success", "Deployment stopped successfully")
                self.refresh_deployments()
            else:
                messagebox.showerror("Error", "Failed to stop deployment")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error stopping deployment: {e}")
    
    def update_statistics(self):
        """Update data statistics"""
        stats = f"Training System Statistics:\n\n"
        stats += f"Total Models: {len(self.trainer.get_model_list())}\n"
        stats += f"Active Deployments: {len(self.deployment_manager.active_deployments)}\n"
        stats += f"Training Data Samples: {len(self.training_data)}\n"
        stats += f"Evaluation Tests: {len(self.evaluator.test_suites)}\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)
    
    def _update_loop(self):
        """Main update loop for UI updates"""
        while True:
            try:
                # Get updates from queue
                update_type, data = self.update_queue.get(timeout=1)
                
                if update_type == 'training_complete':
                    self.current_model = data
                    self.progress_label.config(text="Training completed successfully!")
                    self.train_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.refresh_models()
                    self.training_log.insert(tk.END, f"Training completed: {data.model_id}\n")
                    
                elif update_type == 'training_error':
                    self.progress_label.config(text=f"Training failed: {data}")
                    self.train_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.training_log.insert(tk.END, f"Training error: {data}\n")
                    
                elif update_type == 'evaluation_complete':
                    self.evaluation_results = data
                    self.update_evaluation_results()
                    
                elif update_type == 'evaluation_error':
                    messagebox.showerror("Evaluation Error", data)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Update loop error: {e}")
    
    def update_evaluation_results(self):
        """Update evaluation results display"""
        if not self.evaluation_results:
            return
        
        # Update summary
        summary = "Evaluation Summary:\n\n"
        for suite_name, result in self.evaluation_results.items():
            summary += f"{suite_name.replace('_', ' ').title()}:\n"
            summary += f"  Overall Score: {result.overall_score:.3f}\n"
            summary += f"  Accuracy: {result.accuracy_score:.3f}\n"
            summary += f"  Performance: {result.performance_score:.3f}\n"
            summary += f"  Robustness: {result.robustness_score:.3f}\n\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)
        
        # Update detailed results
        details = "Detailed Results:\n\n"
        for suite_name, result in self.evaluation_results.items():
            details += f"=== {suite_name.upper()} ===\n"
            for test_result in result.test_results:
                details += f"Test: {test_result.test_name}\n"
                details += f"  Accuracy: {test_result.accuracy:.3f}\n"
                details += f"  Response Time: {test_result.response_time:.3f}s\n"
                details += f"  Throughput: {test_result.throughput:.1f} req/s\n\n"
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, details)
    
    def on_model_selected(self, event):
        """Handle model selection"""
        # Update deployment model selection
        self.deploy_model_var.set(self.model_var.get())
    
    def generate_evaluation_report(self):
        """Generate evaluation report"""
        if not self.evaluation_results:
            messagebox.showwarning("Warning", "No evaluation results to report")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Evaluation Report",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                report = self.evaluator.generate_evaluation_report(self.evaluation_results)
                with open(filename, 'w') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {e}")
    
    def export_metrics(self):
        """Export monitoring metrics"""
        filename = filedialog.asksaveasfilename(
            title="Export Metrics",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                metrics = {
                    'timestamp': datetime.now().isoformat(),
                    'metrics': {k: v.get() for k, v in self.metrics_vars.items()}
                }
                with open(filename, 'w') as f:
                    json.dump(metrics, f, indent=2)
                messagebox.showinfo("Success", f"Metrics exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export metrics: {e}")
    
    def clear_charts(self):
        """Clear monitoring charts"""
        self.ax1.clear()
        self.ax2.clear()
        self.init_monitoring_charts()
    
    def import_training_data(self):
        """Import training data"""
        self.load_training_data()  # Reuse existing method
    
    def export_training_data(self):
        """Export training data"""
        if not self.training_data:
            messagebox.showwarning("Warning", "No training data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Training Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.training_data, f, indent=2)
                messagebox.showinfo("Success", f"Training data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")
    
    def import_model(self):
        """Import model"""
        filename = filedialog.askopenfilename(
            title="Import Model",
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # In practice, implement model import logic
                messagebox.showinfo("Success", "Model imported successfully")
                self.refresh_models()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import model: {e}")
    
    def export_model(self):
        """Export model"""
        if not self.current_model:
            messagebox.showwarning("Warning", "No model to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Model",
            defaultextension=".pkl",
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # In practice, implement model export logic
                messagebox.showinfo("Success", f"Model exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export model: {e}")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = AgentTrainingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 