import { AuthenticationForm } from "src/components/form/auth-form";

export const LoginPage = () => {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100vh"
      }}
    >
      <AuthenticationForm />
    </div>
  );
};
