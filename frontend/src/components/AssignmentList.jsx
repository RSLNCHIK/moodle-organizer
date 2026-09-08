function AssignmentList({ assignments, onAssignmentClick }) {
    return (
        <section>
            <h2 className="mb-4 text-xl font-semidbold">
                Assignments:
            </h2>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {assignments.map((assignment) => (
                    <div key={assignment.id}
                    onClick={() => onAssignmentClick(assignment.id)}
                    className="cursor-pointer rounded-xl bg-white p-5 hover:shadow-md">
                        {assignment.name}
                    </div>
                ))}
            </div>

        </section>
    )
}

export default AssignmentList;