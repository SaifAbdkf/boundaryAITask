const DashboardLayout = ({ children }) => {
  return (
    <div>
      <main className="flex h-[100dvh] overflow-hidden w-full">
        <div className="w-full">{children}</div>
      </main>
    </div>
  );
};

export default DashboardLayout;
