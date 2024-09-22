import pandas as pd

# Load the Excel file
file_path = 'path_to_your_file.xlsx'
xls = pd.ExcelFile(file_path)

# Load the sheets with the updated names 'Capacity csv' and 'Volume'
df_capacity_updated = pd.read_excel(xls, sheet_name='Capacity csv')
df_volume_updated = pd.read_excel(xls, sheet_name='Volume')

# Rename columns for easier processing
df_capacity_updated = df_capacity_updated.rename(columns={
    'Capacity (copy)': 'Capacity',
    'Actual PR on Desk': 'Actual_work',
    'PR Target': 'Target',
    'Primary': 'Primary_task',
    'Secondary': 'Secondary_task'
})

# Calculate total tasks per LOB (based on Volume sheet)
total_task_per_lob_updated = df_volume_updated.groupby('Line of Business').agg(total_tasks=('GoldTier', 'count'))

# Group by 'POD' to calculate the sum of Target and Actual work for each manager, along with primary and secondary tasks
capacity_per_manager_updated = df_capacity_updated.groupby('POD').agg(
    total_target=('Target', 'sum'),
    total_actual_work=('Actual_work', 'sum'),
    primary_task=('Primary_task', 'first'),
    secondary_task=('Secondary_task', 'first')
)

# Calculate the capacity: Target - Actual Work
capacity_per_manager_updated['capacity'] = capacity_per_manager_updated['total_target'] - capacity_per_manager_updated['total_actual_work']
capacity_per_manager_updated['capacity'] = capacity_per_manager_updated['capacity'].apply(lambda x: max(x, 0))

# Filter managers who have capacity greater than 0
managers_with_capacity_updated = capacity_per_manager_updated[capacity_per_manager_updated['capacity'] > 0].reset_index()

# Perform primary task allocation
task_allocation_with_names_updated = pd.merge(
    managers_with_capacity_updated,
    total_task_per_lob_updated,
    left_on='primary_task',
    right_on='Line of Business',
    how='inner'
)

# Allocate tasks for primary LOB based on capacity
task_allocation_with_names_updated['allocated_tasks'] = task_allocation_with_names_updated.apply(
    lambda row: min(row['capacity'], row['total_tasks']),
    axis=1
)

# Update capacity and total tasks after primary allocation
updated_capacity_per_manager_updated = capacity_per_manager_updated.copy()
for index, row in task_allocation_with_names_updated.iterrows():
    updated_capacity_per_manager_updated.loc[row['POD'], 'capacity'] -= row['allocated_tasks']
    total_task_per_lob_updated.loc[row['primary_task'], 'total_tasks'] -= row['allocated_tasks']

# Ensure capacity does not drop below 0
updated_capacity_per_manager_updated['capacity'] = updated_capacity_per_manager_updated['capacity'].apply(lambda x: max(x, 0))

# Perform secondary task allocation with remaining capacity
managers_with_remaining_capacity_updated = updated_capacity_per_manager_updated[updated_capacity_per_manager_updated['capacity'] > 0].reset_index()
secondary_task_allocation_updated = pd.merge(
    managers_with_remaining_capacity_updated,
    total_task_per_lob_updated,
    left_on='secondary_task',
    right_on='Line of Business',
    how='inner'
)

# Allocate tasks for secondary LOB based on remaining capacity
secondary_task_allocation_updated['allocated_tasks'] = secondary_task_allocation_updated.apply(
    lambda row: min(row['capacity'], row['total_tasks']),
    axis=1
)

# Update remaining capacity and total tasks after secondary allocation
for index, row in secondary_task_allocation_updated.iterrows():
    updated_capacity_per_manager_updated.loc[row['POD'], 'capacity'] -= row['allocated_tasks']
    total_task_per_lob_updated.loc[row['secondary_task'], 'total_tasks'] -= row['allocated_tasks']

# Ensure capacity does not drop below 0 after secondary allocation
updated_capacity_per_manager_updated['capacity'] = updated_capacity_per_manager_updated['capacity'].apply(lambda x: max(x, 0))

# Combine primary and secondary task allocations into a final table
task_allocation_with_names_updated['primary_tasks_allocated'] = task_allocation_with_names_updated['allocated_tasks']
secondary_task_allocation_updated = secondary_task_allocation_updated[['POD', 'allocated_tasks']].rename(columns={'allocated_tasks': 'secondary_tasks_allocated'})

final_allocation_updated = pd.merge(
    task_allocation_with_names_updated[['POD', 'primary_task', 'primary_tasks_allocated']],
    secondary_task_allocation_updated,
    on='POD',
    how='outer'
)

# Fill missing values for secondary tasks allocated
final_allocation_updated['secondary_tasks_allocated'] = final_allocation_updated['secondary_tasks_allocated'].fillna(0)

# Add updated capacity to the final allocation table
final_allocation_updated = pd.merge(
    final_allocation_updated,
    updated_capacity_per_manager_updated[['capacity']].reset_index(),
    on='POD',
    how='left'
)

# Adding secondary task column to final allocation table
final_allocation_updated_with_secondary_task = pd.merge(
    final_allocation_updated,
    managers_with_capacity_updated[['POD', 'secondary_task']],
    on='POD',
    how='left'
)

# Adding a new column for the total allocation (sum of primary and secondary tasks allocated)
final_allocation_updated_with_secondary_task['total_new_allocation'] = (
    final_allocation_updated_with_secondary_task['primary_tasks_allocated'] +
    final_allocation_updated_with_secondary_task['secondary_tasks_allocated']
)

# Final Task Allocation with Total New Allocation
print("Final Task Allocation With Total New Allocation")
print(final_allocation_updated_with_secondary_task)

# Updated Total Tasks Per LOB (Unassigned Kept)
updated_total_tasks_per_lob = total_task_per_lob_updated.copy()
print("\nUpdated Total Tasks Per LOB (Unassigned Kept)")
print(updated_total_tasks_per_lob)
