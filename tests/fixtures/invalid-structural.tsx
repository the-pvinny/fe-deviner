export function InvalidStructural() {
  return (
    <div style={{ padding: "16px" }} onClick={() => {}}>
      <img src="/photo.jpg" />
      <input type="text" placeholder="Name" />
      <button className="rounded-md p-2">
        <svg aria-hidden="true" />
      </button>
    </div>
  );
}

export default InvalidStructural;
