function FileList({ files }) {
    return (
        <section>
            <h2 className="mb-4 text-xl font-semibold">
                Dateien
            </h2>

            <div className="space-y-3">
                {files.map((file) => (
                    <div key={file.id}
                    className="rounded-xl bg-white p-4 shadow-sm">
                        <p className="font-medium">{file.filename}</p>
                        <p className="text-sm text-gray-500">{file.mimetype}</p>

                    </div>
                ))}
            </div>

        </section>
    )

}
// section is used to create a semantic section of the page that contains the list of files. This is used to group related content together and to improve the accessibility of the page.

export default FileList;