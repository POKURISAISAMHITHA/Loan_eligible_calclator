"""
Database module for SQLite storage
"""
import sqlite3
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager for loan applications"""
    
    def __init__(self, db_path: str = "loan_approval.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_db(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create applications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id TEXT UNIQUE NOT NULL,
                    applicant_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    current_stage TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    application_data TEXT NOT NULL,
                    agent_results TEXT,
                    final_decision TEXT
                )
            """)
            
            # Create agent_logs table for detailed tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    data TEXT,
                    error TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (application_id) REFERENCES applications(application_id)
                )
            """)
            
            # Create indexes for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_application_id 
                ON applications(application_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_agent_logs_app_id 
                ON agent_logs(application_id)
            """)
            
            logger.info("Database initialized successfully")
    
    def create_application(
        self,
        application_id: str,
        applicant_name: str,
        application_data: Dict[str, Any]
    ) -> bool:
        """
        Create a new loan application record
        
        Args:
            application_id: Unique application identifier
            applicant_name: Name of applicant
            application_data: Full application data
            
        Returns:
            bool: True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute("""
                    INSERT INTO applications (
                        application_id, applicant_name, status, current_stage,
                        created_at, updated_at, application_data, agent_results
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    application_id,
                    applicant_name,
                    "pending",
                    "initiated",
                    now,
                    now,
                    json.dumps(application_data),
                    json.dumps({})
                ))
                
                logger.info(f"Created application record: {application_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to create application: {e}")
            return False
    
    def update_stage(self, application_id: str, stage: str) -> bool:
        """
        Update current processing stage
        
        Args:
            application_id: Application ID
            stage: New stage name
            
        Returns:
            bool: True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE applications 
                    SET current_stage = ?, updated_at = ?
                    WHERE application_id = ?
                """, (stage, datetime.now().isoformat(), application_id))
                
                logger.info(f"Updated stage for {application_id}: {stage}")
                return True
        except Exception as e:
            logger.error(f"Failed to update stage: {e}")
            return False
    
    def save_agent_result(
        self,
        application_id: str,
        agent_name: str,
        success: bool,
        data: Dict[str, Any],
        error: Optional[str] = None
    ) -> bool:
        """
        Save agent execution result
        
        Args:
            application_id: Application ID
            agent_name: Name of the agent
            success: Whether agent succeeded
            data: Result data
            error: Error message if failed
            
        Returns:
            bool: True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Log to agent_logs table
                cursor.execute("""
                    INSERT INTO agent_logs (
                        application_id, agent_name, success, data, error, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    application_id,
                    agent_name,
                    1 if success else 0,
                    json.dumps(data),
                    error,
                    datetime.now().isoformat()
                ))
                
                # Update agent_results in applications table
                cursor.execute("""
                    SELECT agent_results FROM applications 
                    WHERE application_id = ?
                """, (application_id,))
                
                row = cursor.fetchone()
                if row:
                    agent_results = json.loads(row[0]) if row[0] else {}
                    agent_results[agent_name] = {
                        "success": success,
                        "data": data,
                        "error": error,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    cursor.execute("""
                        UPDATE applications 
                        SET agent_results = ?, updated_at = ?
                        WHERE application_id = ?
                    """, (
                        json.dumps(agent_results),
                        datetime.now().isoformat(),
                        application_id
                    ))
                
                logger.info(f"Saved result for {agent_name}: {application_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to save agent result: {e}")
            return False
    
    def save_final_decision(
        self,
        application_id: str,
        decision_data: Dict[str, Any]
    ) -> bool:
        """
        Save final loan decision
        
        Args:
            application_id: Application ID
            decision_data: Final decision data
            
        Returns:
            bool: True if successful
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE applications 
                    SET final_decision = ?, status = ?, updated_at = ?
                    WHERE application_id = ?
                """, (
                    json.dumps(decision_data),
                    "completed",
                    datetime.now().isoformat(),
                    application_id
                ))
                
                logger.info(f"Saved final decision for {application_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to save final decision: {e}")
            return False
    
    def get_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve application by ID
        
        Args:
            application_id: Application ID
            
        Returns:
            Optional[Dict]: Application data or None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM applications WHERE application_id = ?
                """, (application_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "application_id": row["application_id"],
                        "applicant_name": row["applicant_name"],
                        "status": row["status"],
                        "current_stage": row["current_stage"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"],
                        "application_data": json.loads(row["application_data"]),
                        "agent_results": json.loads(row["agent_results"]) if row["agent_results"] else {},
                        "final_decision": json.loads(row["final_decision"]) if row["final_decision"] else None
                    }
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve application: {e}")
            return None
    
    def get_agent_logs(self, application_id: str) -> list[Dict[str, Any]]:
        """
        Get all agent logs for an application
        
        Args:
            application_id: Application ID
            
        Returns:
            list: List of agent log entries
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM agent_logs 
                    WHERE application_id = ?
                    ORDER BY timestamp ASC
                """, (application_id,))
                
                rows = cursor.fetchall()
                return [
                    {
                        "agent_name": row["agent_name"],
                        "success": bool(row["success"]),
                        "data": json.loads(row["data"]) if row["data"] else {},
                        "error": row["error"],
                        "timestamp": row["timestamp"]
                    }
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Failed to retrieve agent logs: {e}")
            return []


# Global database instance
db = Database()
