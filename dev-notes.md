# 🧠 Dev Notes — Critical Thinking Warm-Up

## Feature / Fix Name:
*(e.g., Login route, User registration, Input validation update)*

---

<details>
  <summary>1. What could go wrong?</summary>

- *(Think bugs, bad data, security holes, user confusion, scalability issues)*

</details>

<details>
  <summary>2. Tester attack plan (try to break it)</summary>

- *(As a tester, what weird inputs or scenarios would you try? e.g., missing fields, huge payload, wrong type, malicious script)*

</details>

<details>
  <summary>3. After solving / adding this feature:</summary>

**Why does it work?**  
- *(Brief technical reason — “Password hash checked against stored hash in DB”)*

**What could break this?**  
- *(Dependencies, assumptions, future code changes)*

**What risk could this bring?**  
- *(Security, performance, user trust, maintainability)*

</details>

<details>
  <summary>4. Later / Research</summary>

- *(Things to improve or learn more about for future sprints)*

</details>

---

**Entry:**
<details>
<summary>Add category</summary>

## Feature:
Add Category for Expense
### What could go wrong:
- Have to do two migrations. First add the category table and the column for category id in expenses table, make it nullable. Then fill in category for all expenses. Then make another migration to make the column category_id required. 

### After adding this feature:
- Think about what to do if a category is deleted. Where do we want to put its expenses. Or we just not allow deleting categories that have expenses.
- User has not been added yet.
</details>