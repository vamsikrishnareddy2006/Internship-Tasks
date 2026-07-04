# Grade Calculator

print("=== Grade Calculator ===")

# Input marks for 5 subjects
subject1 = float(input("Enter marks for Subject 1: "))
subject2 = float(input("Enter marks for Subject 2: "))
subject3 = float(input("Enter marks for Subject 3: "))
subject4 = float(input("Enter marks for Subject 4: "))
subject5 = float(input("Enter marks for Subject 5: "))

# Calculate total and percentage
total = subject1 + subject2 + subject3 + subject4 + subject5
percentage = total / 5

# Determine grade
if percentage >= 90:
    grade = "A+"
elif percentage >= 80:
    grade = "A"
elif percentage >= 70:
    grade = "B"
elif percentage >= 60:
    grade = "C"
elif percentage >= 50:
    grade = "D"
else:
    grade = "F"

# Display results
print("\n===== Result =====")
print("Total Marks :", total)
print("Percentage  :", percentage, "%")
print("Grade       :", grade)