// @ts-check

import { createFolderStructure } from "eslint-plugin-project-structure";

export const folderStructureConfig = createFolderStructure({
  structure: [
    // Allow any files in the root of your project, like package.json, eslint.config.mjs, etc.
    // You can add rules for them separately.
    // You can also add exceptions like this: "(?!folderStructure)*".
    { name: "*" },

    // Allow any folders in the root of your project.
    { name: "*", children: [] },

    // The `src` folder should follow this structure.
    {
      name: "src",
      children: [
        { name: "index.tsx" },
        { name: "allowAnyFoldersAndFiles", children: [] },

        // src/allowFoldersAndFiles/useSomeHook.ts
        // src/allowFoldersAndFiles/folderName/hello_world.json
        {
          name: "allowFoldersAndFiles",
          children: [
            { name: "use{PascalCase}.(ts|tsx)" },
            { name: "{camelCase}", children: [{ name: "{snake_case}.json" }] }
          ]
        },
        {
          name: "allowOnlyFolders",
          children: [
            {
              name: "{SNAKE_CASE}",
              children: [
                { name: "{kebab-case}.js" },
                { name: "{folderName}.types.ts" }
              ]
            }
          ]
        },
        { name: "allowOnlyFiles", children: [{ name: "{PascalCase}.tsx" }] }
      ]
    }
  ]
});
