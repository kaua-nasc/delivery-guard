import { JSX } from "react/jsx-runtime";

interface HomePageProps {
  children?: string | JSX.Element | JSX.Element[];
}

export const HomePage = ({ children }: HomePageProps): JSX.Element => {
  return <div>{children}</div>;
};
