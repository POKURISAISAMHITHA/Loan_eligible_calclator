#!/bin/bash
# Production Logs Viewer - Quick Access Script

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         📋 Loan Approval System - Production Logs             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if container is running
if ! sudo docker ps | grep -q loan_approval_system; then
    echo -e "${RED}❌ Container is not running!${NC}"
    echo "Start it with: sudo docker compose up -d"
    exit 1
fi

echo -e "${GREEN}✅ Container is running${NC}"
echo ""

# Show menu
echo -e "${YELLOW}Select an option:${NC}"
echo "1) View last 50 lines"
echo "2) Follow logs in real-time (Ctrl+C to stop)"
echo "3) View errors only"
echo "4) View loan applications"
echo "5) View recent activity (last 10 minutes)"
echo "6) Search logs"
echo "7) Save logs to file"
echo "8) View all logs"
echo "9) Show container stats"
echo "0) Exit"
echo ""
read -p "Enter choice [0-9]: " choice

case $choice in
    1)
        echo -e "\n${BLUE}📄 Last 50 lines:${NC}\n"
        sudo docker logs --tail 50 loan_approval_system
        ;;
    2)
        echo -e "\n${BLUE}📡 Following logs in real-time (Press Ctrl+C to stop)...${NC}\n"
        sudo docker logs -f --tail 20 loan_approval_system
        ;;
    3)
        echo -e "\n${BLUE}❌ Errors and Warnings:${NC}\n"
        sudo docker logs loan_approval_system | grep -E "ERROR|WARNING" || echo "No errors found!"
        ;;
    4)
        echo -e "\n${BLUE}📝 Loan Applications:${NC}\n"
        sudo docker logs loan_approval_system | grep -E "Received loan application|Processing complete" | tail -20
        ;;
    5)
        echo -e "\n${BLUE}⏰ Recent activity (last 10 minutes):${NC}\n"
        sudo docker logs --since 10m loan_approval_system | tail -50
        ;;
    6)
        read -p "Enter search term: " search_term
        echo -e "\n${BLUE}🔍 Searching for '${search_term}':${NC}\n"
        sudo docker logs loan_approval_system | grep -i "$search_term" || echo "No matches found!"
        ;;
    7)
        filename="logs_$(date +%Y%m%d_%H%M%S).txt"
        sudo docker logs loan_approval_system > "$filename"
        echo -e "\n${GREEN}✅ Logs saved to: $filename${NC}"
        echo "File size: $(du -h "$filename" | cut -f1)"
        ;;
    8)
        echo -e "\n${BLUE}📄 All logs (this may be long):${NC}\n"
        read -p "Press Enter to continue or Ctrl+C to cancel..."
        sudo docker logs loan_approval_system | less
        ;;
    9)
        echo -e "\n${BLUE}📊 Container Statistics:${NC}\n"
        echo -e "${YELLOW}Container Status:${NC}"
        sudo docker ps --filter name=loan_approval_system --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo -e "${YELLOW}Resource Usage:${NC}"
        sudo docker stats --no-stream loan_approval_system
        echo ""
        echo -e "${YELLOW}Log Statistics:${NC}"
        total_lines=$(sudo docker logs loan_approval_system 2>&1 | wc -l)
        errors=$(sudo docker logs loan_approval_system 2>&1 | grep -c "ERROR" || echo "0")
        warnings=$(sudo docker logs loan_approval_system 2>&1 | grep -c "WARNING" || echo "0")
        applications=$(sudo docker logs loan_approval_system 2>&1 | grep -c "POST /loan/apply" || echo "0")
        echo "Total log lines: $total_lines"
        echo "Errors: $errors"
        echo "Warnings: $warnings"
        echo "Loan applications: $applications"
        ;;
    0)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice!${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
