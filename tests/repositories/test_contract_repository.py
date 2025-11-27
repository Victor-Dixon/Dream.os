#!/usr/bin/env python3
"""
Tests for Contract Repository
==============================

Tests for contract data access layer.

Author: Agent-7
Date: 2025-11-27
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from src.repositories.contract_repository import ContractRepository


class TestContractRepository:
    """Test suite for ContractRepository."""

    @pytest.fixture
    def temp_file(self):
        """Create temporary contracts file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = Path(f.name)
            yield temp_path
            if temp_path.exists():
                temp_path.unlink()

    @pytest.fixture
    def repository(self, temp_file):
        """Create ContractRepository instance."""
        return ContractRepository(str(temp_file))

    def test_initialization(self, repository, temp_file):
        """Test repository initialization."""
        assert repository.contracts_file == temp_file
        assert repository.contracts_file.exists()

    def test_ensure_contracts_file_creates_new(self, temp_file):
        """Test creating new contracts file."""
        if temp_file.exists():
            temp_file.unlink()
        
        repo = ContractRepository(str(temp_file))
        assert repo.contracts_file.exists()
        
        data = repo._load_contracts()
        assert "contracts" in data
        assert "metadata" in data

    def test_load_contracts_existing(self, repository):
        """Test loading existing contracts."""
        test_data = {
            "contracts": [{"contract_id": "test-1", "status": "available"}],
            "metadata": {"version": "1.0"}
        }
        repository._save_contracts(test_data)
        
        loaded = repository._load_contracts()
        assert len(loaded["contracts"]) == 1
        assert loaded["contracts"][0]["contract_id"] == "test-1"

    def test_load_contracts_missing(self, temp_file):
        """Test loading when file doesn't exist."""
        if temp_file.exists():
            temp_file.unlink()
        
        repo = ContractRepository(str(temp_file))
        loaded = repo._load_contracts()
        assert "contracts" in loaded
        assert loaded["contracts"] == []

    def test_save_contracts(self, repository):
        """Test saving contracts."""
        test_data = {
            "contracts": [{"contract_id": "test-1"}],
            "metadata": {"version": "1.0"}
        }
        
        result = repository._save_contracts(test_data)
        assert result is True
        
        loaded = repository._load_contracts()
        assert len(loaded["contracts"]) == 1

    def test_get_contract_exists(self, repository):
        """Test getting existing contract."""
        test_contract = {"contract_id": "test-1", "status": "available"}
        data = {"contracts": [test_contract], "metadata": {"version": "1.0"}}
        repository._save_contracts(data)
        
        contract = repository.get_contract("test-1")
        assert contract is not None
        assert contract["contract_id"] == "test-1"

    def test_get_contract_not_exists(self, repository):
        """Test getting non-existent contract."""
        contract = repository.get_contract("nonexistent")
        assert contract is None

    def test_get_all_contracts(self, repository):
        """Test getting all contracts."""
        test_contracts = [
            {"contract_id": "test-1", "status": "available"},
            {"contract_id": "test-2", "status": "claimed"}
        ]
        data = {"contracts": test_contracts, "metadata": {"version": "1.0"}}
        repository._save_contracts(data)
        
        contracts = repository.get_all_contracts()
        assert len(contracts) == 2

    def test_get_all_contracts_empty(self, repository):
        """Test getting all contracts when none exist."""
        contracts = repository.get_all_contracts()
        assert contracts == []

    def test_update_contract_status(self, repository):
        """Test updating contract status."""
        test_contract = {"contract_id": "test-1", "status": "available"}
        data = {"contracts": [test_contract], "metadata": {"version": "1.0"}}
        repository._save_contracts(data)
        
        result = repository.update_contract_status("test-1", "claimed")
        assert result is True
        
        contract = repository.get_contract("test-1")
        assert contract["status"] == "claimed"

    def test_update_contract_status_not_exists(self, repository):
        """Test updating non-existent contract."""
        result = repository.update_contract_status("nonexistent", "claimed")
        assert result is False

