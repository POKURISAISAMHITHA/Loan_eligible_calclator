#!/bin/bash
# Quick Docker Commands for Loan Approval System

echo "🐳 Loan Approval System - Docker Quick Commands"
echo "================================================"
echo ""

# Check if running
if sudo docker ps | grep -q loan_approval_system; then
    echo "✅ Status: RUNNING"
    echo ""
    echo "📍 Access URLs:"
    echo "   • Main UI:        http://localhost:8000/"
    echo "   • API Docs:       http://localhost:8000/docs"
    echo "   • Health Check:   http://localhost:8000/health"
    echo ""
else
    echo "❌ Status: NOT RUNNING"
    echo ""
fi

echo "🛠️  Quick Commands:"
echo "===================="
echo ""
echo "Start:       sudo docker compose up -d"
echo "Stop:        sudo docker compose down"
echo "Restart:     sudo docker restart loan_approval_system"
echo "Logs:        sudo docker logs -f loan_approval_system"
echo "Status:      sudo docker ps"
echo "Shell:       sudo docker exec -it loan_approval_system bash"
echo "Rebuild:     sudo docker compose up -d --build"
echo ""
echo "🧹 Cleanup:"
echo "==========="
echo "Remove:      sudo docker compose down -v"
echo "Clean all:   sudo docker system prune -a"
echo ""
