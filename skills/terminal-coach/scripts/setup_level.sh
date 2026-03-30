#!/bin/bash
# setup_level.sh - Generates terminal practice scenarios
# Usage: ./setup_level.sh <level_number>

LEVEL=$1
ARENA="$HOME/terminal_practice_arena"

# Safety: Ensure we aren't deleting something important if variable is empty
if [ -z "$ARENA" ]; then
    echo "Error: Arena path is undefined."
    exit 1
fi

# Reset the Arena
echo "Resetting Arena at $ARENA..."
rm -rf "$ARENA"
mkdir -p "$ARENA"

case $LEVEL in
    1)
        echo "Setting up Level 1: Navigation & File Management..."
        cd "$ARENA"
        
        # Create a "messy room" scenario
        mkdir "Documents" "Images" "Music"
        
        # Create random files in the wrong places
        touch "Documents/song.mp3" "Documents/photo.jpg"
        touch "Images/report.txt" "Images/notes.doc"
        touch "Music/invoice.pdf"
        
        # Create a hidden secret
        touch ".secret_stash"
        
        echo "Level 1 Ready!"
        echo "Mission: "
        echo "1. Move all .mp3 files to Music/"
        echo "2. Move all .jpg files to Images/"
        echo "3. Move all text/doc/pdf files to Documents/"
        echo "4. Find the hidden file."
        ;;
        
    2)
        echo "Setting up Level 2: The Investigator (Search & Find)..."
        cd "$ARENA"
        mkdir "Logs" "Evidence"
        
        # Generate dummy logs
        for i in {1..50}; do
            echo "Log entry $i: System normal" > "Logs/system_$i.log"
        done
        
        # Insert the "needle"
        echo "Log entry 42: CRITICAL FAILURE - PASSWORD IS 'hunter2'" > "Logs/system_42.log"
        
        # Create a deep directory structure
        mkdir -p "Evidence/Case_A/Subfolder_B/Deep_C"
        echo "The smoking gun" > "Evidence/Case_A/Subfolder_B/Deep_C/weapon.txt"
        
        echo "Level 2 Ready!"
        echo "Mission:"
        echo "1. Find the log file containing 'CRITICAL FAILURE'"
        echo "2. Find the file named 'weapon.txt' hidden somewhere in Evidence/"
        ;;
        
    3)
        echo "Setting up Level 3: The Gatekeeper (Permissions)..."
        cd "$ARENA"
        
        # Create a "locked" diary
        echo "Dear Diary, I love Linux." > "diary.txt"
        chmod 444 "diary.txt" # Read only
        
        # Create a "broken" script
        echo "#!/bin/bash" > "run_me.sh"
        echo "echo 'SUCCESS: YOU RAN THE SCRIPT!'" >> "run_me.sh"
        chmod 644 "run_me.sh" # Not executable
        
        echo "Level 3 Ready!"
        echo "Mission:"
        echo "1. Try to add 'PS: I also love coding.' to diary.txt (It should fail)."
        echo "2. Fix the permissions so you CAN write to diary.txt."
        echo "3. Try to run ./run_me.sh (It should fail)."
        echo "4. Make the script executable and run it."
        ;;

    4)
        echo "Setting up Level 4: The Data Plumber (Pipes & filters)..."
        cd "$ARENA"
        
        echo "Generating messy server logs..."
        # Generate 100 lines of noise
        for i in {1..100}; do
            echo "192.168.1.$((RANDOM%255)) - - [01/Feb/2026:10:00:$i] \"GET /index.html HTTP/1.1\" 200 1024" >> access.log
        done
        
        # Generate the Attack
        # The Bad Guy is 10.0.0.66
        for i in {1..20}; do
            echo "10.0.0.66 - - [01/Feb/2026:10:05:$i] \"GET /admin.php HTTP/1.1\" 404 0" >> access.log
        done
        # Some decoy errors
        for i in {1..5}; do
            echo "192.168.1.50 - - [01/Feb/2026:10:06:$i] \"GET /image.jpg HTTP/1.1\" 404 0" >> access.log
        done
        
        echo "Level 4 Ready!"
        echo "Mission: Identify the Attacker."
        echo "1. The log file 'access.log' has legitimate traffic and '404' errors."
        echo "2. Find the IP address that generated the MOST '404' errors."
        echo "3. Your final command should output a sorted list of IPs and their error counts."
        echo "   Hint: cat access.log | rg ... | cut ... | sort | uniq -c | sort ..."
        ;;

    5)
        echo "Setting up Level 5: The Assassin (Process Management)..."
        cd "$ARENA"
        
        # Launch a dummy process in the background
        # It's a sleep command disguised as a "mining_virus"
        sleep 1000 &
        PID=$!
        
        # We can't easily rename the process in bash without exec hacks,
        # so we will create a dummy script that RUNS forever.
        echo "#!/bin/bash" > mining_virus.sh
        echo "while true; do sleep 1; done" >> mining_virus.sh
        chmod +x mining_virus.sh
        ./mining_virus.sh &
        
        echo "Level 5 Ready!"
        echo "Mission: TERMINATE THE VIRUS."
        echo "1. A script named 'mining_virus.sh' is running in the background."
        echo "2. Use 'ps aux | rg mining' to find its PID (Process ID)."
        echo "3. Use 'kill <PID>' to stop it."
        echo "4. Verify it's gone with 'ps aux'."
        ;;
        
    *)
        echo "Unknown Level. Available levels: 1, 2"
        exit 1
        ;;
esac
